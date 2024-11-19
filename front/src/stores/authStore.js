import { defineStore } from "pinia";
import axios from "axios";

axios.defaults.baseURL = "http://127.0.0.1:8000/api"; // 전역 기본 URL 설정

export const useAuthStore = defineStore("auth", {
  state: () => ({
    isAuthenticated: !!localStorage.getItem("authToken"), // 로그인 여부
    user: null, // 로그인된 사용자 정보
  }),
  actions: {
    async login(loginData) {
      try {
        const response = await axios.post("/accounts/login/", loginData);
        const token = response.data.token;

        // 토큰 저장 및 상태 업데이트
        localStorage.setItem("authToken", token);
        axios.defaults.headers.common.Authorization = `Token ${token}`;
        this.isAuthenticated = true;
        this.user = response.data.user;
      } catch (error) {
        // 오류 메시지 전달
        if (error.response && error.response.data) {
          throw new Error(error.response.data.error || "아이디 또는 비밀번호가 잘못되었습니다.");
        } else {
          throw new Error("네트워크 오류가 발생했습니다. 다시 시도해주세요.");
        }
      }
    },
    async fetchUserProfile() {
      try {
        // 프로필 API 호출
        const response = await axios.get("/accounts/profile/", {
          headers: { Authorization: `Token ${localStorage.getItem("authToken")}` },
        });

        // 사용자 정보 상태 업데이트
        this.user = response.data;
        return response.data; // 반환
      } catch (error) {
        console.error("프로필 정보를 가져오는 중 오류 발생:", error);
        this.logout(); // 오류 발생 시 로그아웃 처리
        throw error;
      }
    },
    logout() {
      // 토큰 제거 및 상태 초기화
      localStorage.removeItem("authToken");
      delete axios.defaults.headers.common.Authorization;
      this.isAuthenticated = false;
      this.user = null;
    },
  },
});
