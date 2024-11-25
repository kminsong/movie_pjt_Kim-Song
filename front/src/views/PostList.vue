<template>
  <div class="post-list">
    <!-- 검색 창 -->
    <div class="search-bar">
      <!-- 검색 조건 선택 -->
      <select v-model="searchField">
        <option value="title">제목</option>
        <option value="author">작성자</option>
        <option value="content">내용</option>
      </select>
      <!-- 검색 입력 -->
      <input
        v-model="searchQuery"
        type="text"
        placeholder="검색어를 입력하세요"
      />
      <!-- 검색 버튼 -->
      <button @click="fetchPosts">검색</button>
    </div>

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
      posts: [], // 게시글 리스트
      searchQuery: "", // 검색어
      searchField: "title", // 검색 필드 (기본값: 제목)
    };
  },
  methods: {
    async fetchPosts() {
      try {
        const params = {
          filter: this.filter,
          search: this.searchQuery,
          search_field: this.searchField, // 검색 필드 추가
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
.search-bar {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
  gap: 10px; /* 검색 창 간격 */
}

.search-bar select {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

.search-bar input {
  width: 50%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

.search-bar button {
  padding: 10px 20px;
  background-color: #007bff;
  border: none;
  color: white;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
}

.search-bar button:hover {
  background-color: #0056b3;
}

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
post-header .date,
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
