<template>
  <div>
    <h1>리뷰 목록</h1>
    <!-- 검색 영역 -->
    <div>
      <input v-model="searchQuery" placeholder="검색어를 입력하세요" @keyup.enter="performSearch" />
      <select v-model="filterOption">
        <option value="title">리뷰 제목</option>
        <option value="movie_title">영화 제목</option>
        <option value="user_nickname">작성자</option>
      </select>
      <button @click="performSearch">검색</button>
    </div>
    <!-- 정렬 버튼 -->
    <div>
      <button @click="changeOrder('latest')">최신순</button>
      <button @click="changeOrder('likes')">좋아요순</button>
      <button @click="changeOrder('rating')">평점순</button>
    </div>
    <!-- 리뷰 목록 -->
    <div class="review-table">
      <!-- 헤더 설정 -->
      <div class="review-header">
        <span class="title-column">제목</span>
        <span class="rating-column">평점</span>
        <span class="movie-title-column">영화 제목</span>
        <span class="author-column">작성자</span>
        <span class="likes-column">좋아요</span>
        <span class="date-column">작성 날짜</span>
      </div>
      <!-- 리뷰 리스트 설정 -->
      <ul>
        <li
          v-for="review in reviews"
          :key="review.id"
          class="review-row"
          @click="goToReviewDetail(review.id)"
        >
          <span class="title-column">{{ truncateTitle(review.title) }}</span>
          <span class="rating-column">{{ getStarRating(review.star_rating || 0) }}</span>
          <span class="movie-title-column">{{ truncateTitle(review.movie_title || "정보 없음") }}</span>
          <span class="author-column">{{ review.user_nickname }}</span>
          <span class="likes-column">{{ review.like_count }}</span>
          <span class="date-column">{{ formatDate(review.created_at) }}</span>
        </li>
      </ul>
    </div>
    <!-- 페이지네이션 -->
    <div v-if="totalPages > 1" class="pagination">
      <button v-if="currentPage > 1" @click="fetchReviewsByPage(1)">처음</button>
      <button v-if="currentPage > 1" @click="fetchReviewsByPage(currentPage - 1)">이전</button>

      <button
        v-for="page in paginationPages"
        :key="page"
        :class="{ active: currentPage === page }"
        @click="fetchReviewsByPage(page)"
      >
        {{ page }}
      </button>

      <button v-if="currentPage < totalPages" @click="fetchReviewsByPage(currentPage + 1)">다음</button>
      <button v-if="currentPage < totalPages" @click="fetchReviewsByPage(totalPages)">마지막</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      reviews: [], // 리뷰 데이터
      searchQuery: "", // 검색어
      filterOption: "title", // 검색 필터 (리뷰 제목, 영화 제목, 작성자)
      orderBy: "latest", // 정렬 기준
      currentPage: 1, // 현재 페이지
      totalPages: 1, // 총 페이지 수
    };
  },
  methods: {
    // 리뷰 목록 가져오기
    async fetchReviews(page = 1) {
      const params = {
        search: this.searchQuery,
        filter: this.filterOption,
        order_by: this.orderBy,
        page: page,
      };

      try {
        const response = await axios.get("/reviews/", { params });
        this.reviews = response.data.results || [];
        this.currentPage = page;
        this.totalPages = Math.ceil(response.data.count / 10); // 페이지당 10개
      } catch (error) {
        console.error("리뷰 정보를 가져오는 중 오류 발생:", error);
      }
    },
    // 검색 실행
    performSearch() {
      this.currentPage = 1; // 검색 시 첫 페이지로 초기화
      this.fetchReviews();
    },
    // 페이지네이션에서 특정 페이지로 이동
    fetchReviewsByPage(page) {
      this.fetchReviews(page);
    },
    // 정렬 변경
    changeOrder(order) {
      this.orderBy = order;
      this.fetchReviews(); // 정렬 기준 변경 후 다시 가져오기
    },
    // 리뷰 제목 길이 제한
    truncateTitle(title, maxLength = 20) {
      if (title.length > maxLength) {
        return title.slice(0, maxLength) + "...";
      }
      return title;
    },
    // 별점 표시
    getStarRating(rating) {
      const filledStars = Math.floor(rating);
      const halfStar = rating % 1 >= 0.5 ? "★" : "";
      const emptyStars = 5 - filledStars - (halfStar ? 1 : 0);
      return "★".repeat(filledStars) + halfStar + "☆".repeat(emptyStars);
    },
    // 날짜 형식 변환
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
    // 리뷰 상세 페이지로 이동
    goToReviewDetail(reviewId) {
      this.$router.push({ name: "ReviewDetail", params: { id: reviewId } });
    },
  },
  computed: {
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
  created() {
    this.fetchReviews(); // 컴포넌트 생성 시 리뷰 목록 가져오기
  },
};
</script>

<style scoped>
h1 {
  font-size: 24px;
  margin-bottom: 20px;
}

input {
  margin-right: 10px;
  padding: 5px;
}

select {
  margin-right: 10px;
  padding: 5px;
}

button {
  margin-right: 10px;
  padding: 5px 10px;
  background-color: #f1f1f1;
  color: black;
  border: none;
  cursor: pointer;
}

button:disabled {
  background-color: #cccccc;
}

button:hover:not(:disabled) {
  background-color: #0056b3;
}

.review-table {
  margin-top: 20px;
}

/* 리뷰 헤더 스타일 */
.review-header {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  border-bottom: 1px solid #ddd;
  align-items: center;
  font-weight: bold;
  color: black;
  background-color: #f1f1f1;
  margin-left: 20px;
}

/* 리뷰 리스트 스타일 */
.review-row {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  border-bottom: 1px solid #ddd;
  align-items: center;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.review-row:hover {
  background-color: #336eff;
}

.title-column,
.rating-column,
.movie-title-column,
.author-column,
.likes-column,
.date-column {
  flex: 1;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.rating-column {
  flex: 0.8;
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
