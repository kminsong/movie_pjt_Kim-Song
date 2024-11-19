<template>
  <div class="login-container">
    <h1>로그인</h1>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="username">아이디</label>
        <input
          v-model="username"
          id="username"
          type="text"
          placeholder="아이디를 입력하세요"
          required
        />
      </div>
      <div class="form-group">
        <label for="password">비밀번호</label>
        <input
          v-model="password"
          id="password"
          type="password"
          placeholder="비밀번호를 입력하세요"
          required
        />
      </div>
      <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>
      <button :disabled="!isFormValid" type="submit">로그인</button>
    </form>
  </div>
</template>

<script>
import { useAuthStore } from "@/stores/authStore";

export default {
  name: "LoginView",
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
    };
  },
  computed: {
    isFormValid() {
      return this.username.trim() !== "" && this.password.trim() !== "";
    },
  },
  methods: {
    async handleLogin() {
      const loginData = {
        username: this.username,
        password: this.password,
      };

      try {
        const authStore = useAuthStore(); // Pinia 스토어 사용
        await authStore.login(loginData);
        alert("로그인 성공!");
        this.$router.push("/"); // 메인 페이지로 이동
      } catch (error) {
        console.error("로그인 중 오류 발생:", error);
        this.errorMessage = error.message || "로그인에 실패했습니다.";
        this.password = ""; // 비밀번호 필드 초기화
      }
    },
  },
};
</script>

<style scoped>
/* 기존 스타일 유지 */
</style>
