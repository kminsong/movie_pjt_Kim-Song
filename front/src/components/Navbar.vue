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
        <router-link to="/community">Community</router-link>
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
        <button @click="handleLogout" class="logout-button">Logout</button>
      </li>
    </ul>
  </nav>
</template>

<script>
import { useAuthStore } from "@/stores/authStore";

export default {
  name: "Navbar",
  setup() {
    const authStore = useAuthStore();

    const handleLogout = () => {
      authStore.logout();
      window.location.href = "/"; // 새로고침 후 홈 화면으로 이동
    };

    return { authStore, handleLogout };
  },
};
</script>

<style scoped>
.navbar {
  background-color: #333;
  color: white;
  padding: 10px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.navbar-list {
  list-style: none;
  display: flex;
  gap: 20px;
  margin: 0;
  padding: 0;
}

.navbar-item {
  font-size: 1rem;
}

.navbar-item a {
  text-decoration: none;
  color: white;
  transition: color 0.3s ease;
}

.navbar-item a:hover {
  color: #1e90ff; /* 밝은 파란색 */
}

.logout-button {
  background-color: #ff4d4d;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.logout-button:hover {
  background-color: #cc0000; /* 더 어두운 빨간색 */
}
</style>
