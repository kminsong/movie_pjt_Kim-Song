<template>
    <div class="login-container">
      <h1>로그인</h1>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">아이디</label>
          <input v-model="username" id="username" type="text" placeholder="아이디를 입력하세요" required />
        </div>
        <div class="form-group">
          <label for="password">비밀번호</label>
          <input v-model="password" id="password" type="password" placeholder="비밀번호를 입력하세요" required />
        </div>
        <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>
        <button type="submit">로그인</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        username: "",
        password: "",
        errorMessage: "", // 로그인 실패 시 보여줄 메시지
      };
    },
    methods: {
      handleLogin() {
        const loginData = {
          username: this.username,
          password: this.password,
        };
  
        axios
          .post("/api/accounts/login/", loginData)
          .then((response) => {
            alert("로그인 성공!");
            localStorage.setItem("authToken", response.data.token); // 토큰 저장
            this.$router.push("/"); // 메인 페이지로 이동
          })
          .catch((error) => {
            console.error("로그인 중 오류 발생:", error);
            this.errorMessage = "아이디 또는 비밀번호가 잘못되었습니다."; // 오류 메시지 업데이트
          });
      },
    },
  };
  </script>
  
  <style scoped>
  .login-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 5px;
  }
  
  .error-text {
    color: red;
    font-size: 0.8em;
  }
  
  button[type="submit"] {
    width: 100%;
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
  }
  
  button[type="submit"]:hover {
    background-color: #0056b3;
  }
  </style>
  