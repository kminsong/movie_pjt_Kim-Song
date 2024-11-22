import { createApp } from "vue";
import App from "./App.vue";
import { createPinia } from "pinia";
import router from "./router";
import axios from "axios"; // axios 추가

// axios 기본 URL 설정
axios.defaults.baseURL = "http://127.0.0.1:8000/api";

// Pinia 및 Router 초기화
const pinia = createPinia();

createApp(App)
  .use(pinia) // Pinia 등록
  .use(router) // Router 등록
  .mount("#app");
