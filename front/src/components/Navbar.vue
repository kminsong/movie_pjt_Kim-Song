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
      <li class="navbar-item" v-if="!authStore.isAuthenticated">
        <router-link to="/login">Login</router-link>
      </li>
      <li class="navbar-item" v-if="!authStore.isAuthenticated">
        <router-link to="/register">Register</router-link>
      </li>
      <li class="navbar-item" v-if="authStore.isAuthenticated">
        <router-link to="/profile">My Page</router-link>
      </li>
      <li class="navbar-item" v-if="authStore.isAuthenticated">
        <button @click="authStore.logout" class="logout-button">Logout</button>
      </li>
    </ul>
  </nav>
</template>

<script>
import { useAuthStore } from "@/stores/authStore";

export default {
  name: "Navbar",
  setup() {
    const authStore = useAuthStore(); // Pinia 상태 사용
    return { authStore };
  },
};
</script>

<style scoped>
/* 기존 스타일 유지 */
</style>
