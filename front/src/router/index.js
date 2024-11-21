import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import AboutView from "@/views/AboutView.vue";
import MoviesView from "@/views/MoviesView.vue";
import MovieDetailView from "@/views/MovieDetailView.vue";
import ReviewsView from "@/views/ReviewsView.vue";
import LoginView from "@/views/LoginView.vue"; // 로그인 페이지 추가
import RegisterView from "@/views/RegisterView.vue"; // 회원가입 페이지 추가
import ProfileView from "@/views/ProfileView.vue"; // 마이페이지 추가
import ProfileEditView from "@/views/ProfileEditView.vue";

const routes = [
  { path: "/", name: "Home", component: HomeView },
  { path: "/about", name: "About", component: AboutView },
  { path: "/movies", name: "Movies", component: MoviesView },
  {
    path: "/reviews/:id",
    name: "ReviewDetail",
    component: () => import("@/views/ReviewDetailView.vue"),
  },
  { path: "/movies/:id", name: "MovieDetail", component: MovieDetailView },
  { path: "/reviews", name: "Reviews", component: ReviewsView },
  { path: "/login", name: "Login", component: LoginView }, // 로그인 경로 추가
  { path: "/register", name: "Register", component: RegisterView }, // 회원가입 경로 추가
  { path: "/profile", name: "Profile", component: ProfileView }, // 마이페이지 경로 추가
  { path: "/profile/edit", name: "ProfileEdit", component: ProfileEditView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
