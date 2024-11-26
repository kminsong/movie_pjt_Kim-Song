<template>
  <nav class="navbar">
    <ul class="navbar-list">
      <!-- 좌측(중앙) 메뉴 -->
      <div class="navbar-center">
        <li class="navbar-item logo-item">
          <router-link to="/">
            <img src="@/assets/skynetflix.jpg" alt="Skynetflix Logo" class="logo-image" />
          </router-link>
        </li>
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
      </div>

      <!-- 우측 메뉴 -->
      <div class="navbar-right">
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
      </div>
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
  background-color: #7e0e0e; /* 어두운 배경 */
  color: #eaeaea; /* 밝은 텍스트 */
  padding: 10px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.6); /* 그림자 효과 */
  height: 60px;
}

.navbar-list {
  display: flex;
  width: 100%;
  justify-content: space-between;
  margin: 0;
  padding: 0;
  list-style: none;
}

.navbar-list li {
  font-weight: bold; /* 글자 굵기 증가 */
  font-size: large;
}

.navbar-center {
  display: flex;
  gap: 20px;
  align-items: center;
}

.navbar-right {
  display: flex;
  gap: 15px;
  align-items: center;
}

.navbar-item {
  font-size: 1rem;
}

.navbar-item a {
  text-decoration: none;
  color: #eaeaea; /* 기본 텍스트 색상 */
  transition: color 0.3s ease, transform 0.2s ease;
}

.navbar-item a:hover {
  color: #ff4d4d; /* 붉은 포인트 */
  transform: scale(1.1); /* 살짝 확대 */
}

.logout-button {
  background-color: #5166c4;
  color: #ffffff; /* 흰색 텍스트 */
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: large;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.logout-button:hover {
  background-color: #5572f3;
  transform: scale(1.1); /* 살짝 확대 */
}

.logo-item {
  margin-right: 10px;
}

.logo-image {
  width: 40px; /* 이미지 크기 */
  height: 40px;
  border-radius: 50%; /* 동그라미 모양 */
  object-fit: cover; /* 이미지 비율 유지 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5); /* 그림자 효과 */
}
</style>
