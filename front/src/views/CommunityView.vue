<template>
  <div class="community">
    <h1>커뮤니티</h1>

    <!-- 전체글, Hot, 게시글 작성하기 -->
    <div class="controls">
      <button @click="goToAllPosts" :class="{ active: isAllPosts }">전체글</button>
      <button @click="goToHotPosts" :class="{ active: isHotPosts }">Hot</button>
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

    <PostList :isHot="isHotPosts" :filter="filter" />
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
      isAuthenticated: false, // 로그인 상태 확인
    };
  },
  computed: {
    isAllPosts() {
      return !this.isHotPosts;
    },
  },
  created() {
    // 로그인 상태 확인
    this.isAuthenticated = !!localStorage.getItem("authToken");
  },
  methods: {
    goToAllPosts() {
      this.isHotPosts = false;
    },
    goToHotPosts() {
      this.isHotPosts = true;
    },
    goToPostForm() {
      this.$router.push({ name: "PostCreate" });
    },
    showLoginAlert() {
      alert("로그인 후 게시글을 작성할 수 있습니다.");
    },
    applyFilter() {},
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

.controls button.active {
  background-color: #28a745;
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
</style>
