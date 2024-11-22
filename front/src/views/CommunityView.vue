<template>
  <div class="community">
    <h1>커뮤니티</h1>

    <!-- 전체글, Hot, 게시글 작성하기 -->
    <div class="controls">
      <button @click="goToAllPosts" :class="{ active: isAllPosts }">전체글</button>
      <button @click="goToHotPosts" :class="{ active: isHotPosts }">Hot</button>
      <button
        v-if="canWritePost"
        @click="goToPostForm"
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
    };
  },
  computed: {
    isAllPosts() {
      return !this.isHotPosts;
    },
    canWritePost() {
      return true; // 로그인 여부에 따라 수정 가능
    },
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
