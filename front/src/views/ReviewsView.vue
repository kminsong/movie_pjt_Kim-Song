<template>
  <div>
    <h1>리뷰 목록</h1>
    <!-- 검색 영역 -->
    <div>
      <input v-model="searchQuery" placeholder="검색어를 입력하세요" />
      <select v-model="filterOption">
        <option value="title">리뷰 제목</option>
        <option value="movie_title">영화 제목</option>
      </select>
      <button @click="fetchReviews">검색</button>
    </div>
    <!-- 정렬 버튼 -->
    <div>
      <button @click="changeOrder('latest')">최신순</button>
      <button @click="changeOrder('likes')">좋아요순</button>
    </div>
    <!-- 리뷰 목록 -->
    <div>
      <ul>
        <li v-for="review in reviews" :key="review.id">
          <h3>{{ review.title }}</h3>
          <p><strong>영화 제목:</strong> {{ review.movie_title || '정보 없음' }}</p>
          <p><strong>내용:</strong> {{ review.content }}</p>
          <p><strong>좋아요:</strong> {{ review.like_count }}</p>
        </li>
      </ul>
    </div>
    <!-- 페이지네이션 -->
    <div v-if="pagination">
      <button :disabled="!pagination.previous" @click="fetchReviews(pagination.previous)">
        이전
      </button>
      <button :disabled="!pagination.next" @click="fetchReviews(pagination.next)">
        다음
      </button>
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
      filterOption: "title", // 검색 필터 (리뷰 제목 또는 영화 제목)
      orderBy: "latest", // 정렬 기준
      pagination: null, // 페이지네이션 정보
    };
  },
  methods: {
    // 리뷰 목록 가져오기
    fetchReviews(url = "/reviews/") {
      const params = {
        search: this.searchQuery,
        filter: this.filterOption,
        order_by: this.orderBy,
      };

      axios
        .get(url, { params })
        .then((response) => {
          this.reviews = response.data.results || [];
          this.pagination = response.data.pagination || null;
        })
        .catch((error) => {
          console.error("리뷰 정보를 가져오는 중 오류 발생:", error);
        });
    },
    // 정렬 변경
    changeOrder(order) {
      this.orderBy = order;
      this.fetchReviews(); // 정렬 기준 변경 후 다시 가져오기
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
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

button:disabled {
  background-color: #cccccc;
}

button:hover:not(:disabled) {
  background-color: #0056b3;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}
</style>
