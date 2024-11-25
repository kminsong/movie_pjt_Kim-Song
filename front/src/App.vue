<template>
  <div id="app" class="app-background">
    <Navbar />
    <router-view />
  </div>
</template>

<script>
import Navbar from "./components/Navbar.vue";

export default {
  name: "App",
  components: {
    Navbar,
  },
};
</script>

<style>
/* 전역 배경 스타일 */
.app-background {
  background: linear-gradient(to bottom, #1c1c1c, #101010); /* 어두운 그라데이션 */
  color: #eaeaea; /* 밝은 텍스트 */
  min-height: 100vh; /* 화면 전체 높이 */
  margin: 0;
  padding: 0;
  font-family: "Roboto", sans-serif; /* 전역 폰트 */
}
</style>
