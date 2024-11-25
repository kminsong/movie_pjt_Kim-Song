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

<style>
/* 전역 배경 스타일 */
body {
  margin: 0;
  padding: 0;
  background-color: #000000; /* 완전 검정 배경 */
  font-family: "Roboto", sans-serif;
  color: #eaeaea;
}

/* 로그인 박스 스타일 */
.login-container {
  background: #2c2c2c; /* 연한 회색 배경 */
  color: #eaeaea;
  padding: 30px;
  border-radius: 10px;
  max-width: 400px;
  margin: 100px auto; /* 중앙 정렬 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5); /* 그림자 효과 */
  text-align: center;
}

/* 로그인 제목 */
.login-container h1 {
  color: #00bcd4; /* 청록색 포인트 */
  font-size: 2rem;
  margin-bottom: 20px;
  text-shadow: 0 0 10px #00bcd4;
}

/* 입력 필드와 폼 그룹 */
.form-group {
  margin-bottom: 20px;
  text-align: left;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #eaeaea;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 5px;
  background-color: #404040; /* 어두운 입력 필드 */
  color: #eaeaea;
  font-size: 1rem;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.6);
}

.form-group input::placeholder {
  color: #a9a9a9; /* 플레이스홀더 텍스트 */
}

.form-group input:focus {
  outline: none;
  border: 1px solid #00bcd4; /* 청록색 포커스 */
}

/* 에러 메시지 */
.error-text {
  color: #ff5555; /* 에러 메시지는 붉은 색 */
  font-size: 0.9rem;
  margin-top: -10px;
  margin-bottom: 15px;
}

/* 버튼 스타일 */
button {
  background-color: #00bcd4;
  color: #101010; /* 버튼 텍스트 어두운 색 */
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

button:disabled {
  background-color: #555; /* 비활성화 버튼 색상 */
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #00a5b8; /* 호버 시 버튼 색상 변경 */
  transform: scale(1.05);
}
</style>
