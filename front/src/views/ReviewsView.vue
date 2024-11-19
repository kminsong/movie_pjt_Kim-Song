<template>
    <div>
      <h1>전체 리뷰</h1>
      <!-- 검색 및 필터 기능 -->
      <div class="search-filters">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="검색어를 입력하세요"
        />
        <select v-model="filterBy">
          <option value="title">제목</option>
          <option value="movie_title">영화 제목</option>
        </select>
        <select v-model="orderBy">
          <option value="latest">최신순</option>
          <option value="likes">좋아요순</option>
        </select>
        <button @click="fetchReviews">검색</button>
      </div>
  
      <!-- 리뷰 목록 -->
      <div v-if="reviews && reviews.length > 0">
        <div v-for="review in reviews" :key="review.id" class="review-item">
          <h3>{{ review.title || "제목 없음" }}</h3>
          <p>댓글 수: {{ review.comment_count || 0 }}</p>
          <p>영화 제목: {{ review.movie_title || "정보 없음" }}</p>
        </div>
      </div>
      <p v-else>
        {{ searchQuery ? "검색 결과가 없습니다." : "리뷰가 없습니다." }}
      </p>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        reviews: [], // 리뷰 데이터 초기화
        searchQuery: "", // 검색어
        filterBy: "title", // 검색 필터 (제목, 영화 제목)
        orderBy: "latest", // 정렬 기준 (최신순, 좋아요순)
      };
    },
    created() {
      this.fetchReviews();
    },
    methods: {
      fetchReviews() {
        const params = {
          search: this.searchQuery,
          filter: this.filterBy,
          order_by: this.orderBy, // 백엔드와 일치하는 키로 설정
        };
        axios
          .get("/api/reviews/", { params })
          .then((response) => {
            // 응답 데이터를 검증하고 설정
            this.reviews = Array.isArray(response.data.results)
              ? response.data.results
              : [];
          })
          .catch((error) => {
            console.error("리뷰 데이터를 가져오는 중 오류 발생:", error);
            this.reviews = []; // 오류 발생 시 빈 배열로 설정
          });
      },
    },
  };
  </script>
  
  <style scoped>
  .search-filters {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
  }
  
  .review-item {
    border: 1px solid #ccc;
    padding: 10px;
    margin-bottom: 10px;
  }
  </style>
  