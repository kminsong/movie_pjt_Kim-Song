<template>
  <div class="community">
    <h1>커뮤니티</h1>

    <!-- 전체글, Hot, 게시글 작성하기 -->
    <div class="controls">
      <button @click="switchToAllPosts" :class="{ active: isAllPosts }">전체글</button>
      <button @click="switchToHotPosts" :class="{ active: isHotPosts }" class="hot-button">Hot</button>
      <button
        v-if="isAuthenticated"
        @click="goToPostForm"
        class="write-button"
      >
        게시글 작성하기
      </button>
      <button
        v-else
        @click="showLoginAlert"
        class="write-button"
      >
        게시글 작성하기
      </button>
    </div>

    <!-- 필터 추가 -->
    <div class="filters">
      <label>
        <input
          type="radio"
          value="latest"
          v-model="filter"
          @change="applyFilter"
        /> 최신순
      </label>
      <label>
        <input
          type="radio"
          value="likes"
          v-model="filter"
          @change="applyFilter"
        /> 좋아요순
      </label>
      <label>
        <input
          type="radio"
          value="comments"
          v-model="filter"
          @change="applyFilter"
        /> 댓글순
      </label>
    </div>

    <!-- 게시글 리스트 -->
    <PostList
      ref="postList"
      :isHot="isHotPosts"
      :filter="filter"
      @click-post="handlePostClick"
      @update-pagination="updatePagination"
    />

    <!-- 페이지네이션 -->
    <div class="pagination">
      <button v-if="currentPage > 1" @click="fetchPostsByPage(1)">처음</button>
      <button v-if="currentPage > 1" @click="fetchPostsByPage(currentPage - 1)">이전</button>

      <button
        v-for="page in paginationPages"
        :key="page"
        :class="{ active: currentPage === page }"
        @click="fetchPostsByPage(page)"
      >
        {{ page }}
      </button>

      <button v-if="currentPage < totalPages" @click="fetchPostsByPage(currentPage + 1)">다음</button>
      <button v-if="currentPage < totalPages" @click="fetchPostsByPage(totalPages)">마지막</button>
    </div>
  </div>
</template>

<script>
import PostList from "@/views/PostList.vue";

export default {
  name: "CommunityView",
  components: {
    PostList,
  },
  data() {
    return {
      isHotPosts: false,
      filter: "latest",
      currentPage: 1,
      totalPages: 1,
      isAuthenticated: false, // 로그인 상태 확인
    };
  },
  computed: {
    isAllPosts() {
      return !this.isHotPosts;
    },
    paginationPages() {
      const range = 2; // 현재 페이지를 기준으로 양쪽 2개 페이지 표시
      const start = Math.max(1, this.currentPage - range);
      const end = Math.min(this.totalPages, this.currentPage + range);
      const pages = [];
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      return pages;
    },
  },
  methods: {
    switchToAllPosts() {
      this.isHotPosts = false; // 상태 변경
      this.$nextTick(() => {
        this.fetchPostsByPage(1); // 상태 변경 후 즉시 데이터 갱신
      });
    },
    switchToHotPosts() {
      this.isHotPosts = true; // 상태 변경
      this.$nextTick(() => {
        this.fetchPostsByPage(1); // 상태 변경 후 즉시 데이터 갱신
      });
    },
    goToPostForm() {
      this.$router.push({ name: "PostCreate" });
    },
    redirectToLogin() {
      alert("로그인 후 이용해주세요.");
      this.$router.push({ name: "Login" });
    },
    handlePostClick(postId) {
      if (!this.isAuthenticated) {
        this.redirectToLogin();
      } else {
        this.$router.push({ name: "PostDetail", params: { id: postId } });
      }
    },
    showLoginAlert() {
      alert("로그인 후 게시글을 작성할 수 있습니다.");
    },
    applyFilter() {
      this.fetchPostsByPage(1);
    },
    updatePagination(data) {
      this.currentPage = data.currentPage;
      this.totalPages = data.totalPages;
    },
    fetchPostsByPage(page) {
      this.currentPage = page;
      this.$refs.postList.fetchPosts(page);
    },
  },
  created() {
    this.isAuthenticated = !!localStorage.getItem("authToken");
  },
};
</script>

<style scoped>
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
.hot-button {
  background-color: #ff4933;
  color: black;
}
.controls button.active {
  background-color: #28a745;
  color: white;
}
.controls button:hover {
  background-color: #336eff;
  color: white;
}
.filters {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
  gap: 10px;
}
.filters label {
  cursor: pointer;
}
.write-button {
  background-color: #ffc107;
  color: black;
}
.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
.pagination button {
  margin: 0 5px;
  padding: 5px 10px;
  border: 1px solid #007bff;
  background-color: white;
  color: #007bff;
  cursor: pointer;
}
.pagination button.active {
  background-color: #007bff;
  color: white;
}
.pagination button:hover {
  background-color: #0056b3;
  color: white;
}
</style>
