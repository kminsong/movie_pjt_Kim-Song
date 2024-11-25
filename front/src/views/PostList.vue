<template>
  <div class="post-list">
    <div class="post-table">
      <!-- 헤더 -->
      <div class="post-header">
        <span class="title">제목</span>
        <span class="author">작성자</span>
        <span class="comments">댓글 수</span>
        <span class="likes">좋아요 수</span>
        <span class="date">작성 날짜</span>
      </div>

      <!-- 게시글 리스트 -->
      <ul>
        <li
          v-for="post in posts"
          :key="post.id"
          :class="{ hot: post.is_hot }"
          @click="goToPostDetail(post.id)"
        >
          <span class="title" :title="post.title">{{ truncateText(post.title, 30) }}</span>
          <span class="author">{{ post.author_name }}</span>
          <span class="comments">{{ post.comment_count }}</span>
          <span class="likes">{{ post.likes }}</span>
          <span class="date">{{ formatDate(post.created_at) }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import api from "@/api/axios";

export default {
  name: "PostList",
  props: ["isHot", "filter"],
  data() {
    return {
      posts: [],
    };
  },
  methods: {
    async fetchPosts() {
      try {
        const params = {
          filter: this.filter,
        };
        if (this.isHot) {
          params.is_hot = true;
        }
        const response = await api.get("/community/posts/", { params });
        this.posts = response.data;
      } catch (error) {
        console.error("게시글 불러오기 실패:", error);
      }
    },
    goToPostDetail(postId) {
      this.$router.push({ name: "PostDetail", params: { id: postId } });
    },
    formatDate(datetime) {
      const now = new Date();
      const createdAt = new Date(datetime);
      const diff = now - createdAt; // 차이(ms 단위)

      const seconds = Math.floor(diff / 1000);
      const minutes = Math.floor(seconds / 60);
      const hours = Math.floor(minutes / 60);
      const days = Math.floor(hours / 24);

      if (days > 0) {
        return `${days}일 전`;
      } else if (hours > 0) {
        return `${hours}시간 전`;
      } else if (minutes > 0) {
        return `${minutes}분 전`;
      } else {
        return `방금 전`;
      }
    },
    truncateText(text, maxLength) {
      return text.length > maxLength ? `${text.slice(0, maxLength)}...` : text;
    },
  },
  watch: {
    isHot: "fetchPosts",
    filter: "fetchPosts",
  },
  created() {
    this.fetchPosts();
  },
};
</script>

<style scoped>
.post-table {
  margin-top: 20px;
}

.post-header,
ul li {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.post-header span,
ul li span {
  flex: 1;
  text-align: center;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

/* 제목 좌측 정렬 */
.post-header .title,
ul li .title {
  flex: 3; /* 제목은 더 넓게 */
  text-align: left; /* 좌측 정렬 */
  padding-left: 10px; /* 좌측 여백 추가 */
}

.post-header .author,
ul li .author,
.post-header .comments,
ul li .comments,
.post-header .likes,
ul li .likes,
.post-header .date,
ul li .date {
  flex: 1; /* 나머지는 작게 */
}

/* Hot 게시글 스타일 */
ul li.hot .title {
  color: red;
  font-weight: bold;
}

ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

ul li {
  cursor: pointer;
}

ul li:hover {
  background-color: #f9f9f9;
}
</style>
