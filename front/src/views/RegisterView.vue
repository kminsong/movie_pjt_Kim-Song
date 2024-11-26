<template>
  <div class="register-container">
    <h1>회원가입</h1>
    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label for="username">
          아이디
          <span class="required">*</span>
        </label>
        <input
          v-model="username"
          id="username"
          type="text"
          placeholder="아이디를 입력하세요"
          @blur="username && checkField('username', username)"
          required
        />
        <p v-if="usernameError" class="error-text">다른 아이디를 입력해 주세요.</p>
        <p v-if="!usernameError && usernameValid" class="success-text">
          사용할 수 있습니다.
        </p>
      </div>

      <div class="form-group">
        <label for="nickname">
          닉네임
          <span class="required">*</span>
        </label>
        <input
          v-model="nickname"
          id="nickname"
          type="text"
          placeholder="닉네임을 입력하세요"
          @blur="nickname && checkField('nickname', nickname)"
          required
        />
        <p v-if="nicknameError" class="error-text">다른 닉네임을 입력해 주세요.</p>
        <p v-if="!nicknameError && nicknameValid" class="success-text">
          사용할 수 있습니다.
        </p>
      </div>

      <div class="form-group">
        <label for="password">
          비밀번호
          <span class="required">*</span>
        </label>
        <input
          v-model="password"
          id="password"
          type="password"
          placeholder="비밀번호를 입력하세요"
          @input="checkPasswordMatch"
          required
        />
      </div>

      <div class="form-group">
        <label for="confirmPassword">
          비밀번호 확인
          <span class="required">*</span>
        </label>
        <input
          v-model="confirmPassword"
          id="confirmPassword"
          type="password"
          placeholder="비밀번호를 다시 입력하세요"
          @input="checkPasswordMatch"
          required
        />
        <p v-if="!isPasswordMatch && confirmPassword" class="error-text">
          비밀번호가 일치하지 않습니다.
        </p>
        <p v-if="isPasswordMatch && confirmPassword" class="success-text">
          비밀번호가 일치합니다.
        </p>
      </div>

      <div class="form-group">
        <label for="email">이메일</label>
        <input
          v-model="email"
          id="email"
          type="email"
          placeholder="이메일을 입력하세요"
          @blur="email && checkField('email', email)"
        />
        <p v-if="emailError" class="error-text">다른 이메일을 입력해 주세요.</p>
        <p v-if="!emailError && emailValid" class="success-text">
          사용할 수 있습니다.
        </p>
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
      confirmPassword: "",
      nickname: "",
      email: "",
      usernameError: false,
      usernameValid: false,
      nicknameError: false,
      nicknameValid: false,
      emailError: false,
      emailValid: false,
      isPasswordMatch: false,
    };
  },
  computed: {
    isFormValid() {
      return (
        this.username &&
        this.password &&
        this.nickname &&
        this.isPasswordMatch &&
        this.usernameValid &&
        this.nicknameValid
      )
    },
  },
  methods: {
    async checkField(field, value) {
      if (!value.trim()) {
        this[`${field}Error`] = "값을 입력해주세요.";
        this[`${field}Valid`] = false;
        return;
      }

      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/api/accounts/check-${field}/`,
          {
            params: { field: field, [field]: value }, // field와 value 전달
          }
        );

        if (response.data.is_available) {
          this[`${field}Error`] = null;
          this[`${field}Valid`] = true;
        } else {
          this[`${field}Error`] = `이미 사용 중인 ${field}입니다.`;
          this[`${field}Valid`] = false;
        }
      } catch (error) {
        console.error(`${field} 중복 검사 중 오류 발생:`, error);
        this[`${field}Error`] = "서버 오류가 발생했습니다. 다시 시도해주세요.";
        this[`${field}Valid`] = false;
      }
    },
    checkPasswordMatch() {
      this.isPasswordMatch = this.password === this.confirmPassword;
    },
    async handleRegister() {
      try {
        const userData = {
          username: this.username,
          password: this.password,
          nickname: this.nickname,
        };

        if (this.email) {
          userData.email = this.email; // 이메일이 입력된 경우에만 추가
        }

        const response = await axios.post(
          "http://127.0.0.1:8000/api/accounts/register/",
          userData
        );

        alert("회원가입 성공! 로그인 페이지로 이동합니다.");
        this.$router.push("/login");
      } catch (error) {
        console.error("회원가입 중 오류 발생:", error);
        alert("회원가입에 실패했습니다. 다시 시도해주세요.");
      }
    },
  },
};
</script>

<style scoped>
body {
  margin: 0;
  padding: 0;
  background-color: #000000; /* 완전 검정 배경 */
  font-family: "Roboto", sans-serif;
  color: #eaeaea;
}

/* 회원가입 박스 스타일 */
.register-container {
  background: #2c2c2c; /* 연한 회색 배경 */
  color: #eaeaea;
  padding: 30px;
  border-radius: 10px;
  max-width: 400px;
  margin: 100px auto; /* 중앙 정렬 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5); /* 그림자 효과 */
  text-align: center;
}

/* 회원가입 제목 */
.register-container h1 {
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

.required {
  color: red;
  font-size: 1rem; /* 크기 조정 */
}
</style>
