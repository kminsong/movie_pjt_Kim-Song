<template>
  <nav class="navbar">
    <ul class="navbar-list">
      <li class="navbar-item">
        <router-link to="/">Home</router-link>
      </li>
      <li class="navbar-item">
        <router-link to="/about">About</router-link>
      </li>
      <li class="navbar-item">
        <router-link to="/movies">Movies</router-link>
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

.navbar-item a {
  color: white;
  text-decoration: none;
  font-weight: 600;
}

.navbar-item a:hover {
  text-decoration: underline;
}
</style>
