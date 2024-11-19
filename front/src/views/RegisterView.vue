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
  
        <div class="form-group">
          <label>좋아하는 장르 (3개 선택 필수)</label>
          <div class="genre-list">
            <button
              v-for="genre in genres"
              :key="genre.id"
              :class="{ selected: selectedGenres.includes(genre.id) }"
              @click="toggleGenre(genre.id)"
              type="button"
            >
              {{ genre.name }}
            </button>
          </div>
          <p v-if="selectedGenres.length !== 3" class="error-text">
            좋아하는 장르를 3개 선택해주세요.
          </p>
        </div>
  
        <button type="submit" :disabled="!isFormValid">회원가입</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  import tmdb from "@/api/tmdb";
  
  export default {
    data() {
      return {
        username: "",
        password: "",
        nickname: "",
        email: "",
        genres: [], // TMDB API로 가져올 장르 데이터
        selectedGenres: [], // 선택된 장르
      };
    },
    computed: {
      isFormValid() {
        return (
          this.username &&
          this.password &&
          this.nickname &&
          this.email &&
          this.selectedGenres.length === 3
        );
      },
    },
    created() {
      this.fetchGenres();
    },
    methods: {
      fetchGenres() {
        tmdb
          .get("/genre/movie/list", { params: { language: "ko-KR" } })
          .then((response) => {
            this.genres = response.data.genres;
          })
          .catch((error) => {
            console.error("장르 데이터를 가져오는 중 오류 발생:", error);
          });
      },
      toggleGenre(genreId) {
        if (this.selectedGenres.includes(genreId)) {
          this.selectedGenres = this.selectedGenres.filter((id) => id !== genreId);
        } else if (this.selectedGenres.length < 3) {
          this.selectedGenres.push(genreId);
        }
      },
      async handleRegister() {
        try {
          const userData = {
            username: this.username,
            password: this.password,
            nickname: this.nickname,
            email: this.email,
            favorite_genres: this.selectedGenres,
          };
  
          console.log("전송 데이터:", userData); // 디버깅 추가
  
          const response = await axios.post(
            "http://127.0.0.1:8000/api/accounts/register/", // 백엔드 API 경로
            userData
          );
  
          console.log("응답 데이터:", response.data); // 디버깅 추가
  
          alert("회원가입 성공!");
          localStorage.setItem("authToken", response.data.token);
          this.$router.push("/"); // 회원가입 후 홈으로 이동
        } catch (error) {
          console.error("회원가입 중 오류 발생:", error);
  
          if (error.response) {
            const { status, data } = error.response;
            console.error("서버 응답 상태:", status, "응답 데이터:", data); // 디버깅 추가
  
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
  /* 스타일 그대로 유지 */
  </style>
  