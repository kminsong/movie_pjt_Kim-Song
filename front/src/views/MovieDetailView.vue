<template>
    <div>
      <h1>{{ movie?.title || "영화 제목 없음" }}</h1>
      <img :src="getPosterPath(movie?.poster_path)" alt="poster" />
      <p><strong>개봉일:</strong> {{ movie?.release_date || "정보 없음" }}</p>
      <p><strong>평점:</strong> {{ movie?.vote_average || "정보 없음" }}</p>
      <p><strong>줄거리:</strong> {{ movie?.overview || "정보 없음" }}</p>
  
      <h3>리뷰</h3>
  
      <!-- 리뷰 작성 버튼 -->
      <button v-if="isAuthenticated" @click="toggleReviewForm">
        {{ showReviewForm ? "작성 취소" : "리뷰 작성하기" }}
      </button>
      <div v-if="showReviewForm">
        <input v-model="reviewTitle" placeholder="리뷰 제목" />
        <textarea v-model="reviewContent" placeholder="리뷰 내용을 작성하세요"></textarea>
        <button @click="submitReview">작성</button>
      </div>
      <p v-else-if="!isAuthenticated">로그인 후 리뷰를 작성할 수 있습니다.</p>
  
      <!-- 리뷰 표시 -->
      <div v-if="reviews.length > 0">
        <ul>
          <li v-for="review in topReviews" :key="review.id">
            <strong>{{ review.title || "제목 없음" }}</strong> - 좋아요: {{ review.like_count || 0 }}
          </li>
        </ul>
      </div>
      <p v-else>리뷰가 없습니다</p>
    </div>
  </template>
  
  <script>
  import tmdb from "@/api/tmdb";
  import axios from "axios";
  
  export default {
    data() {
      return {
        movie: null, // 영화 기본 정보
        reviews: [], // 전체 리뷰
        topReviews: [], // 좋아요 순 상위 3개 리뷰
        isAuthenticated: false, // 로그인 여부 확인
        showReviewForm: false, // 리뷰 작성 폼 표시 여부
        reviewTitle: "", // 작성 중인 리뷰 제목
        reviewContent: "", // 작성 중인 리뷰 내용
      };
    },
    created() {
      const movieId = this.$route.params.id;
      console.log("영화 ID:", movieId); // 디버깅: 영화 ID 확인
      if (movieId) {
        this.fetchMovieDetails(movieId);
        this.fetchReviews(movieId);
      } else {
        console.error("영화 ID가 유효하지 않습니다.");
      }
      this.isAuthenticated = !!localStorage.getItem("authToken"); // 간단한 로그인 상태 확인
    },
    methods: {
      fetchMovieDetails(movieId) {
        tmdb
          .get(`/movie/${movieId}`, { params: { language: "ko-KR" } })
          .then((response) => {
            this.movie = response.data;
          })
          .catch((error) => {
            console.error("영화 정보를 가져오는 중 오류 발생:", error);
          });
      },
      fetchReviews(movieId) {
        axios
          .get(`/api/reviews/?movie_id=${movieId}`)
          .then((response) => {
            this.reviews = Array.isArray(response.data) ? response.data : [];
            // 좋아요 순으로 상위 3개 리뷰 필터링
            this.topReviews = this.reviews
              .sort((a, b) => b.like_count - a.like_count) // 좋아요 순 정렬
              .slice(0, 3); // 상위 3개 선택
          })
          .catch((error) => {
            console.error("리뷰 정보를 가져오는 중 오류 발생:", error);
            this.reviews = []; // 오류 발생 시 빈 배열로 초기화
          });
      },
      toggleReviewForm() {
        this.showReviewForm = !this.showReviewForm;
      },
      submitReview() {
        const newReview = {
          movie_id: this.movie.id,
          title: this.reviewTitle,
          content: this.reviewContent,
        };
        axios
          .post("/api/reviews/", newReview, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("authToken")}`,
            },
          })
          .then(() => {
            alert("리뷰가 작성되었습니다!");
            this.fetchReviews(this.movie.id); // 리뷰 목록 갱신
            this.reviewTitle = "";
            this.reviewContent = "";
            this.showReviewForm = false;
          })
          .catch((error) => {
            console.error("리뷰 작성 중 오류 발생:", error);
          });
      },
      getPosterPath(path) {
        return path
          ? `https://image.tmdb.org/t/p/w500${path}`
          : "https://via.placeholder.com/500x750?text=No+Image";
      },
    },
  };
  </script>
  
  <style scoped>
  h1 {
    font-size: 24px;
    margin-bottom: 10px;
  }
  
  img {
    max-width: 300px;
    height: auto;
  }
  
  ul {
    list-style-type: none;
    padding: 0;
  }
  
  li {
    margin-bottom: 10px;
  }
  </style>
  