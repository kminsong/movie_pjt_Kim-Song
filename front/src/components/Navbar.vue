<template>
  <nav class="navbar">
    <ul class="navbar-list left">
      <li class="navbar-item">
        <router-link to="/">Home</router-link>
      </li>
      <li class="navbar-item">
        <router-link to="/about">About</router-link>
      </li>
    </ul>
    <ul class="navbar-list right">
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
export default {
  name: "Navbar",
};
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background-color: #333; /* 배경색 */
  color: white; /* 텍스트 색 */
  display: flex;
  justify-content: space-between; /* 좌우 정렬 */
  align-items: center;
  padding: 0.5rem 1rem;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1); /* 그림자 효과 */
  z-index: 1000;
}

.navbar-list {
  display: flex;
  list-style: none;
  padding: 0;
  margin: 0;
}

.navbar-list.left {
  margin-right: auto; /* 좌측 정렬 */
}

.navbar-list.right {
  margin-left: auto; /* 우측 정렬 */
}

.navbar-item {
  margin: 0 1rem; /* 항목 간 간격 */
}

.navbar-item a {
  text-decoration: none; /* 밑줄 제거 */
  color: white; /* 링크 텍스트 색 */
  font-weight: bold;
  transition: color 0.3s;
}

.navbar-item a:hover {
  color: #00aced; /* 호버 효과 */
}

.logout-button {
  background: none;
  border: none;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: color 0.3s;
}

.logout-button:hover {
  color: #ff5c5c; /* 로그아웃 버튼 호버 색 */
}
</style>
