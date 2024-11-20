<template>
  <div>
    <!-- 영화 정보 -->
    <h1>{{ movie?.title || "영화 제목 없음" }}</h1>
    <img :src="getPosterPath(movie?.poster_path)" alt="poster" />
    <p><strong>개봉일:</strong> {{ movie?.release_date || "정보 없음" }}</p>
    <p><strong>평점:</strong> {{ movie?.vote_average || "정보 없음" }}</p>
    <p><strong>줄거리:</strong> {{ movie?.overview || "정보 없음" }}</p>

    <!-- 리뷰 작성 및 목록 -->
    <h3>리뷰</h3>
    <button v-if="isAuthenticated" @click="toggleReviewForm">
      {{ showReviewForm ? "작성 취소" : "리뷰 작성하기" }}
    </button>
    <div v-if="showReviewForm">
      <input v-model="reviewTitle" placeholder="리뷰 제목" />
      <textarea v-model="reviewContent" placeholder="리뷰 내용을 작성하세요"></textarea>
      <button @click="submitReview">작성</button>
    </div>
    <p v-else-if="!isAuthenticated">로그인 후 리뷰를 작성할 수 있습니다.</p>

    <div v-if="reviews.length > 0">
      <ul>
        <li v-for="review in topReviews" :key="review.id">
          <strong>{{ review.title || "제목 없음" }}</strong> - 좋아요: {{ review.like_count || 0 }}
        </li>
      </ul>
    </div>
    <p v-else>리뷰가 없습니다</p>

    <!-- 뒤로가기 버튼 -->
    <button @click="goBack">뒤로가기</button>
  </div>
</template>

<script>
import tmdb from "@/api/tmdb";
import axios from "axios";

export default {
  data() {
    return {
      movie: null, // 현재 영화 데이터
      reviews: [], // 전체 리뷰 목록
      topReviews: [], // 상위 3개 리뷰
      isAuthenticated: false, // 로그인 여부
      showReviewForm: false, // 리뷰 작성 폼 표시 여부
      reviewTitle: "", // 리뷰 제목
      reviewContent: "", // 리뷰 내용
    };
  },
  created() {
    const movieId = this.$route.params.id;

    if (movieId) {
      this.fetchMovieDetails(movieId); // 영화 상세 정보 가져오기
      this.fetchReviews(movieId); // 영화 리뷰 가져오기
    } else {
      console.error("영화 ID가 유효하지 않습니다.");
    }

    this.isAuthenticated = !!localStorage.getItem("authToken"); // 토큰으로 로그인 상태 확인
  },
  methods: {
    goBack() {
      // 뒤로가기 버튼 동작
      this.$router.go(-1); // 이전 페이지로 이동
    },
    fetchMovieDetails(movieId) {
      // TMDB에서 영화 상세 정보 가져오기
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
      // 백엔드에서 해당 영화 리뷰 가져오기
      axios
        .get(`/reviews/?movie_id=${movieId}`)
        .then((response) => {
          this.reviews = response.data.results || [];
          this.getTopReviews(); // 상위 3개 리뷰 필터링
        })
        .catch((error) => {
          console.error("리뷰 정보를 가져오는 중 오류 발생:", error);
        });
    },
    getTopReviews() {
      this.topReviews = this.reviews
        .sort((a, b) => {
          if (b.like_count === a.like_count) {
            return new Date(b.created_at) - new Date(a.created_at); // 좋아요 같으면 최신순
          }
          return b.like_count - a.like_count; // 좋아요 많은 순
        })
        .slice(0, 3); // 최대 3개만
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
        .post("/reviews/", newReview, {
          headers: {
            Authorization: `Token ${localStorage.getItem("authToken")}`,
          },
        })
        .then(() => {
          alert("리뷰가 작성되었습니다!");
          this.reviewTitle = "";
          this.reviewContent = "";
          this.showReviewForm = false;
          this.fetchReviews(this.movie.id); // 리뷰 작성 후 목록 갱신
        })
        .catch((error) => {
          console.error(
            "리뷰 작성 중 오류 발생:",
            error.response?.data || error.message
          );
          alert("리뷰 작성에 실패했습니다.");
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

button {
  margin-bottom: 10px;
  padding: 10px;
  border: none;
  background-color: #007bff;
  color: white;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
