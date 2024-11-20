import { defineStore } from "pinia";
import axios from "axios";

axios.defaults.baseURL = "http://127.0.0.1:8000/api";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    isAuthenticated: !!localStorage.getItem("authToken"),
    user: null,
  }),
  actions: {
    async login(loginData) {
      try {
        const response = await axios.post("/accounts/login/", loginData);
        const token = response.data.token;

        localStorage.setItem("authToken", token);
        axios.defaults.headers.common.Authorization = `Token ${token}`;
        this.isAuthenticated = true;
        this.user = response.data.user;
      } catch (error) {
        if (error.response && error.response.data) {
          throw new Error(error.response.data.error || "아이디 또는 비밀번호가 잘못되었습니다.");
        } else {
          throw new Error("네트워크 오류가 발생했습니다. 다시 시도해주세요.");
        }
      }
    },
    async fetchUserProfile() {
      try {
        const response = await axios.get("/accounts/profile/", {
          headers: { Authorization: `Token ${localStorage.getItem("authToken")}` },
        });

        this.user = response.data;
        return response.data;
      } catch (error) {
        console.error("프로필 정보를 가져오는 중 오류 발생:", error);
        this.logout();
        throw error;
      }
    },
    logout() {
      localStorage.removeItem("authToken");
      delete axios.defaults.headers.common.Authorization;
      this.isAuthenticated = false;
      this.user = null;
    },
  },
});
