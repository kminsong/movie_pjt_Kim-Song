<template>
  <div class="community">
    <h1>커뮤니티</h1>
    <!-- 카테고리 버튼 -->
    <div class="categories">
      <button
        v-for="cat in categories"
        :key="cat.name"
        :class="{ active: currentCategory === cat.name }"
        @click="goToCategory(cat.name)"
      >
        {{ cat.name }}
      </button>
    </div>

    <!-- 전체글, Hot, 게시글 작성하기 -->
    <div class="controls">
      <button @click="goToAllPosts" :class="{ active: isAllPosts }">전체글</button>
      <button @click="goToHotPosts" :class="{ active: isHotPosts }">Hot</button>
      <!-- 게시글 작성하기 버튼 -->
      <button
        v-if="canWritePost"
        @click="goToPostForm"
        class="write-button"
      >
        게시글 작성하기
      </button>
    </div>

    <!-- 게시글 리스트 -->
    <PostList :category="currentCategory" :isHot="isHotPosts" />
  </div>
</template>

<script>
import { useAuthStore } from "@/stores/authStore";
import PostList from "@/views/PostList.vue"; // 경로 수정

export default {
  name: "CommunityView",
  components: {
    PostList,
  },
  data() {
    return {
      categories: [
        { name: "공지사항" },
        { name: "영화토론방" },
        { name: "영화수다방" },
        { name: "잡담방" },
      ],
      currentCategory: "공지사항", // 초기 카테고리
      isHotPosts: false, // Hot 글 보기 여부
    };
  },
  computed: {
    isAuthenticated() {
      const authStore = useAuthStore();
      return authStore.isAuthenticated; // 로그인 여부
    },
    isAdmin() {
      const authStore = useAuthStore();
      return authStore.user?.is_superuser || false; // 관리자인지 여부
    },
    canWritePost() {
      // 게시글 작성 조건
      if (this.currentCategory === "공지사항") {
        return this.isAuthenticated && this.isAdmin; // 공지사항은 관리자만
      }
      return this.isAuthenticated; // 나머지 카테고리는 로그인된 사용자
    },
    isAllPosts() {
      return !this.isHotPosts;
    },
  },
  methods: {
    goToCategory(category) {
      this.currentCategory = category;
      this.isHotPosts = false;
    },
    goToAllPosts() {
      this.isHotPosts = false;
    },
    goToHotPosts() {
      this.isHotPosts = true;
    },
    goToPostForm() {
      this.$router.push({ name: "PostForm", query: { category: this.currentCategory } });
    },
  },
};
</script>

<style scoped>
.categories {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.categories button {
  margin: 0 10px;
  padding: 10px 20px;
  border: none;
  cursor: pointer;
}

.categories button.active {
  background-color: #007bff;
  color: white;
}

.controls {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.controls button {
  margin: 0 10px;
  padding: 10px 20px;
  border: none;
  cursor: pointer;
}

.controls button.active {
  background-color: #28a745;
  color: white;
}

.write-button {
  background-color: #ffc107;
  color: black;
}
</style>
