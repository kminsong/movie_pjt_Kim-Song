<template>
    <div>
      <h1>마이페이지</h1>
      <div v-if="user">
        <p><strong>아이디:</strong> {{ user.username }}</p>
        <p><strong>닉네임:</strong> {{ user.nickname }}</p>
        <p><strong>이메일:</strong> {{ user.email }}</p>
        <p>
          <strong>좋아하는 장르:</strong>
          <span v-for="genre in user.favoriteGenres" :key="genre.id">
            {{ genre.name }}
          </span>
        </p>
      </div>
      <div v-else>
        <p>로그인 후 이용 가능합니다.</p>
      </div>
      <button @click="logout">로그아웃</button>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        user: null, // 사용자 정보
      };
    },
    created() {
      this.fetchUserProfile();
    },
    methods: {
      fetchUserProfile() {
        const token = localStorage.getItem("authToken");
        if (!token) {
          alert("로그인이 필요합니다!");
          this.$router.push("/login");
          return;
        }
  
        axios
          .get("/api/accounts/profile/", {
            headers: { Authorization: `Token ${token}` },
          })
          .then((response) => {
            this.user = response.data;
          })
          .catch((error) => {
            console.error("프로필 정보를 가져오는 중 오류 발생:", error.response.data);
            alert("사용자 정보를 불러오지 못했습니다. 다시 로그인 해주세요.");
            this.$router.push("/login");
          });
      },
      logout() {
        localStorage.removeItem("authToken"); // 토큰 삭제
        alert("로그아웃 되었습니다.");
        this.$router.push("/");
      },
    },
  };
  </script>
  
  <style scoped>
  h1 {
    margin-bottom: 20px;
  }
  
  button {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  </style>
  