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
          @click="handlePostClick(post.id)"
        >
          <span class="title" :title="post.title">{{ truncateText(post.title, 30) }}</span>
          <span class="author">{{ post.author_name }}</span>
          <span class="comments">{{ post.comment_count }}</span>
          <span class="likes">{{ post.likes }}</span>
          <span class="date">{{ formatDate(post.created_at) }}</span>
        </li>
      </ul>
    </div>

    <!-- 검색 창 -->
    <div class="search-bar">
      <select v-model="searchField">
        <option value="title">제목</option>
        <option value="author">작성자</option>
        <option value="content">내용</option>
      </select>
      <input
        v-model="searchQuery"
        type="text"
        placeholder="검색어를 입력하세요"
        @keyup.enter="searchPosts"
      />
      <button @click="searchPosts">검색</button>
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
      currentPage: 1, // 현재 페이지
      totalPages: 1, // 총 페이지 수
      isAuthenticated: false,
    };
  },
  methods: {
    async fetchPosts(page = 1) {
      try {
        const params = {
          filter: this.filter,
          search: this.searchQuery.trim(), // 검색어의 공백 제거
          search_field: this.searchField, // 검색 필드
          page: page, // 페이지 번호
        };
        if (this.isHot) {
          params.is_hot = true;
        }

        const response = await api.get("/community/posts/", { params });
        this.posts = response.data.results || [];
        this.currentPage = page;
        this.totalPages = Math.ceil(response.data.count / 10); // 페이지 수 계산
        this.$emit("update-pagination", { currentPage: this.currentPage, totalPages: this.totalPages });
      } catch (error) {
        console.error("게시글 불러오기 실패:", error);
      }
    },
    searchPosts() {
      this.fetchPosts(1); // 검색 시 페이지를 1로 초기화
    },
    handlePostClick(postId) {
      if (!this.isAuthenticated) {
        alert("로그인 후 이용해주세요.");
        this.$router.push({ name: "Login" });
      } else {
        this.goToPostDetail(postId);
      }
    },
    goToPostDetail(postId) {
      this.$router.push({ name: "PostDetail", params: { id: postId } });
    },
    formatDate(datetime) {
      const now = new Date();
      const createdAt = new Date(datetime);
      const diff = now - createdAt;

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
    this.isAuthenticated = !!localStorage.getItem("authToken");
    this.fetchPosts();
  },
};
</script>

<style scoped>
.search-bar {
  position: absolute; /* 좌측 하단 고정 */
  bottom: 20px;
  left: 20px;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px; /* 작아진 검색창 폰트 */
}

.search-bar select,
.search-bar input {
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.search-bar input {
  width: 150px; /* 검색 입력창 크기 축소 */
}

.search-bar button {
  padding: 5px 10px;
  background-color: #007bff;
  border: none;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  font-size: 12px; /* 작아진 버튼 폰트 */
}

.search-bar button:hover {
  background-color: #0056b3;
}
.post-table {
  margin-top: 20px;
  width: 100%; /* 테이블 너비를 100%로 설정 */

}

.post-header,
ul li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 15px; /* 좌우 여백 추가 */
  border-bottom: 1px solid #ddd;
}

.post-header {
  background-color: #f1f1f1; /* 어두운 배경 */
  color: black; /* 밝은 글씨 색 */
  font-weight: bold; /* 헤더 글씨 강조 */
  margin-left: 20px;
}

ul li {
  transition: background-color 0.3s ease;
  color: #eaeaea; /* 리스트 글씨 색 */
  
  margin-left: 30px;
}

ul li:hover {
  background-color: #336eff; /* hover 시 배경색 변경 */
}

.post-header span,
ul li span {
  flex: 1; /* 각 칸 너비 균등 */
  text-align: center; /* 텍스트 중앙 정렬 */
  white-space: nowrap; /* 텍스트 줄바꿈 방지 */
  overflow: hidden; /* 넘치는 텍스트 숨김 */
  text-overflow: ellipsis; /* 넘치는 텍스트 생략(...) */
}
.post-header span{
  color: black;
}

/* .post-header, */
ul li .title {
  flex: 3; /* 제목 칸 더 넓게 설정 */
  display: flex;
  align-items: center;
  justify-content: flex-start; /* 가로 정렬: 좌측 */
  text-align: left; /* 제목은 좌측 정렬 */
  padding-left: 10px; /* 제목 좌측 여백 */
  margin: 0;
  font-size: 16px;
}

.post-header .title {
  flex: 3;
  font-size: 16px; /* 제목 헤더 폰트 크기를 18px로 설정 */
  margin : 1px;
}
ul li.hot .title {
  color: #ff4933;
  font-weight: bold;
}
ul li.hot {
  background-color: #2c2c2c;
  color: #ff4933;
  font-weight: bold;
}
ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
</style>
