import { createApp } from "vue";
import App from "./App.vue";
import { createPinia } from "pinia";
import router from "./router";

const pinia = createPinia();

createApp(App)
  .use(pinia) // Pinia 등록
  .use(router) // Router 등록
  .mount("#app");
