import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import CommunityView from "@/views/CommunityView.vue"; // 커뮤니티 메인 페이지
import PostDetailView from "@/views/PostDetailView.vue"; // 게시글 상세 페이지
import PostForm from "@/views/PostForm.vue"; // 게시글 작성 및 수정 페이지
import MoviesView from "@/views/MoviesView.vue";
import MovieDetailView from "@/views/MovieDetailView.vue";
import ReviewsView from "@/views/ReviewsView.vue";
import LoginView from "@/views/LoginView.vue";
import RegisterView from "@/views/RegisterView.vue";
import ProfileView from "@/views/ProfileView.vue";
import ProfileEditView from "@/views/ProfileEditView.vue";

const routes = [
  { path: "/", name: "Home", component: HomeView },
  { path: "/community", name: "Community", component: CommunityView }, // 커뮤니티 메인 페이지
  { path: "/community/post/:id", name: "PostDetail", component: PostDetailView }, // 게시글 상세 페이지
  { path: "/community/post/:id/edit", name: "PostEdit", component: PostForm }, // 게시글 수정 페이지
  { path: "/community/new", name: "PostCreate", component: PostForm }, // 게시글 작성 페이지
  { path: "/movies", name: "Movies", component: MoviesView },
  { path: "/movies/:id", name: "MovieDetail", component: MovieDetailView },
  { path: "/reviews", name: "Reviews", component: ReviewsView },
  { path: "/reviews/:id", name: "ReviewDetail", component: () => import("@/views/ReviewDetailView.vue") },
  { path: "/login", name: "Login", component: LoginView }, // 로그인 페이지 추가
  { path: "/register", name: "Register", component: RegisterView }, // 회원가입 페이지 추가
  { path: "/profile", name: "Profile", component: ProfileView }, // 마이페이지 경로 추가
  { path: "/profile/edit", name: "ProfileEdit", component: ProfileEditView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
