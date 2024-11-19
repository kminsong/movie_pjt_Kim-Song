<template>
  <div class="register-container">
    <h1>회원가입</h1>
    <form @submit.prevent="handleRegister">
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

      <div class="form-group">
        <label for="nickname">닉네임</label>
        <input
          v-model="nickname"
          id="nickname"
          type="text"
          placeholder="닉네임을 입력하세요"
          required
        />
        <button type="button" @click="checkNickname">중복 검사</button>
        <p v-if="isNicknameAvailable === true" class="success-text">
          닉네임을 사용할 수 있습니다!
        </p>
        <p v-if="isNicknameAvailable === false" class="error-text">
          닉네임이 이미 사용 중입니다.
        </p>
      </div>

      <div class="form-group">
        <label for="email">이메일</label>
        <input
          v-model="email"
          id="email"
          type="email"
          placeholder="이메일을 입력하세요"
          required
        />
      </div>

      <button type="submit" :disabled="!isFormValid">회원가입</button>
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
      nickname: "",
      email: "",
      isNicknameAvailable: null, // 닉네임 중복 상태
    };
  },
  computed: {
    isFormValid() {
      return this.username && this.password && this.nickname && this.email;
    },
  },
  methods: {
    async checkNickname() {
      if (!this.nickname.trim()) {
        alert("닉네임을 입력해주세요.");
        return;
      }

      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/api/accounts/check-nickname/", // 닉네임 중복 검사 API 경로
          {
            params: { nickname: this.nickname },
          }
        );

        this.isNicknameAvailable = response.data.is_available;
        if (this.isNicknameAvailable) {
          alert("닉네임을 사용할 수 있습니다.");
        } else {
          alert("닉네임이 이미 사용 중입니다.");
        }
      } catch (error) {
        console.error("닉네임 중복 검사 중 오류 발생:", error);
        alert("닉네임 중복 검사에 실패했습니다. 다시 시도해주세요.");
      }
    },
    async handleRegister() {
      try {
        const userData = {
          username: this.username,
          password: this.password,
          nickname: this.nickname,
          email: this.email,
        };

        console.log("전송 데이터:", userData);

        const response = await axios.post(
          "http://127.0.0.1:8000/api/accounts/register/", // 회원가입 API 경로
          userData
        );

        console.log("응답 데이터:", response.data);

        alert("회원가입 성공!");
        localStorage.setItem("authToken", response.data.token);
        this.$router.push("/");
      } catch (error) {
        console.error("회원가입 중 오류 발생:", error);

        if (error.response) {
          const { status, data } = error.response;
          console.error("서버 응답 상태:", status, "응답 데이터:", data);

          if (status === 400 && data) {
            alert("입력한 정보를 확인해주세요.");
          } else {
            alert("회원가입에 실패했습니다. 다시 시도해주세요.");
          }
        } else {
          alert("네트워크 오류가 발생했습니다. 서버 상태를 확인하세요.");
        }
      }
    },
  },
};
</script>

<style scoped>
.success-text {
  color: green;
  font-weight: bold;
  margin-top: 5px;
}

.error-text {
  color: red;
  font-weight: bold;
  margin-top: 5px;
}
</style>
