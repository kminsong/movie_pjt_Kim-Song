<template>
    <div class="edit-profile-container">
      <h1>회원 정보 수정</h1>
      <form @submit.prevent="updateProfile">
        <div class="form-group">
          <label for="username">아이디</label>
          <input
            v-model="user.username"
            id="username"
            type="text"
            placeholder="아이디를 입력하세요"
            disabled
          />
        </div>
        <div class="form-group">
          <label for="nickname">닉네임</label>
          <input
            v-model="user.nickname"
            id="nickname"
            type="text"
            placeholder="닉네임을 입력하세요"
            required
          />
        </div>
        <div class="form-group">
          <label for="email">이메일</label>
          <input
            v-model="user.email"
            id="email"
            type="email"
            placeholder="이메일을 입력하세요"
            required
          />
        </div>
        <button type="submit">저장</button>
        <button type="button" @click="goBack">취소</button>
      </form>
    </div>
  </template>
  
  <script>
  import { useAuthStore } from "@/stores/authStore";
  import axios from "axios";
  
  export default {
    name: "ProfileEditView",
    data() {
      return {
        user: {
          username: "",
          nickname: "",
          email: "",
        },
      };
    },
    async created() {
      const authStore = useAuthStore();
  
      if (!authStore.isAuthenticated) {
        alert("로그인이 필요합니다!");
        this.$router.push("/login");
        return;
      }
  
      try {
        const profile = await authStore.fetchUserProfile();
        this.user = {
          username: profile.username,
          nickname: profile.nickname,
          email: profile.email,
        };
      } catch (error) {
        console.error("프로필 정보를 가져오는 중 오류 발생:", error);
        alert("사용자 정보를 불러오지 못했습니다. 다시 로그인 해주세요.");
        authStore.logout();
        this.$router.push("/login");
      }
    },
    methods: {
      async updateProfile() {
        try {
          await axios.put("/accounts/profile/", this.user, {
            headers: {
              Authorization: `Token ${localStorage.getItem("authToken")}`,
            },
          });
          alert("회원 정보가 성공적으로 수정되었습니다.");
          this.$router.push("/profile");
        } catch (error) {
          console.error("회원 정보 수정 중 오류 발생:", error);
          alert("회원 정보 수정에 실패했습니다. 다시 시도해주세요.");
        }
      },
      goBack() {
        this.$router.push("/profile");
      },
    },
  };
  </script>
  
  <style scoped>
  .edit-profile-container {
    max-width: 500px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 8px;
  }
  
  h1 {
    text-align: center;
    margin-bottom: 20px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    font-weight: bold;
    margin-bottom: 5px;
  }
  
  input {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  button {
    padding: 10px 15px;
    margin-right: 10px;
    border: none;
    background-color: #007bff;
    color: white;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  
  button[type="button"] {
    background-color: #dc3545;
  }
  
  button[type="button"]:hover {
    background-color: #a71d2a;
  }
  </style>
  