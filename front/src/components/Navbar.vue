<template>
  <nav class="navbar">
    <ul class="navbar-list">
      <li class="navbar-item">
        <router-link to="/">Home</router-link>
      </li>
      <li class="navbar-item">
        <router-link to="/movies">Movies</router-link>
      </li>
      <li class="navbar-item">
        <router-link to="/reviews">Reviews</router-link>
      </li>
      <li class="navbar-item">
        <router-link to="/about">About</router-link>
      </li>
      <!-- 로그인 상태에 따라 조건부 렌더링 -->
      <li class="navbar-item" v-if="!isAuthenticated">
        <router-link to="/login">Login</router-link>
      </li>
      <li class="navbar-item" v-if="!isAuthenticated">
        <router-link to="/register">Register</router-link>
      </li>
      <li class="navbar-item" v-if="isAuthenticated">
        <router-link to="/profile">My Page</router-link>
      </li>
      <li class="navbar-item" v-if="isAuthenticated">
        <button @click="logout" class="logout-button">Logout</button>
      </li>
    </ul>
  </nav>
</template>

<script>
import { ref } from "vue";

export default {
  name: "Navbar",
  setup() {
    // 로그인 상태 확인 (토큰 유무로 판단)
    const isAuthenticated = ref(!!localStorage.getItem("authToken"));

    // 로그아웃 로직
    const logout = () => {
      localStorage.removeItem("authToken"); // 토큰 삭제
      isAuthenticated.value = false; // 상태 업데이트
      alert("로그아웃 되었습니다.");
    };

    return { isAuthenticated, logout };
  },
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #333;
  color: white;
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
}

.navbar-list {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
}

.navbar-item {
  margin-right: 20px;
}

.navbar-item:last-child {
  margin-right: 0;
}

.navbar-item a {
  color: white;
  text-decoration: none;
  font-weight: 600;
}

.navbar-item a:hover {
  text-decoration: underline;
}

.logout-button {
  background: none;
  border: none;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

.logout-button:hover {
  text-decoration: underline;
}
</style>
