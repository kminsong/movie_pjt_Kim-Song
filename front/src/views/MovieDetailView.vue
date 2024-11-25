<template>
  <div>
    <!-- 영화 상세 -->
    <div class="movie-detail">
      <!-- 포스터 -->
      <div class="poster">
        <img :src="getPosterPath(movie?.poster_path)" alt="poster" />
      </div>

      <!-- 영화 정보 -->
      <div class="info">
        <h1>{{ movie?.title || "영화 제목 없음" }}</h1>
        <p><strong>개봉일:</strong> {{ movie?.release_date || "정보 없음" }}</p>
        <p><strong>평점:</strong> {{ movie?.vote_average || "정보 없음" }}</p>
        <p><strong>리뷰 평점:</strong> <span v-html="getStarRating(movieAverageRating)"></span></p>
        <p><strong>줄거리:</strong> {{ movie?.overview || "정보 없음" }}</p>
        <div class="genres-container">
          <p
            v-for="genre in movie?.genres"
            :key="genre.id"
            @click="goToMoviesByGenre(genre.id)"
            class="clickable-genre"
          >
            #{{ genre.name }}
          </p>
        </div>
      </div>
    </div>

    <!-- 리뷰 작성 및 목록 -->
    <h3>리뷰</h3>
    <button v-if="isAuthenticated" @click="toggleReviewForm">
      {{ showReviewForm ? "작성 취소" : "리뷰 작성하기" }}
    </button>
    <div v-if="showReviewForm" class="review-form">
      <label for="review-title">리뷰 제목</label>
      <input id="review-title" v-model="reviewTitle" placeholder="리뷰 제목" />
      <label for="review-content">리뷰 내용</label>
      <textarea
        id="review-content"
        v-model="reviewContent"
        placeholder="리뷰 내용을 작성하세요"
      ></textarea>
      <div class="rating">
        <label>별점:</label>
        <div class="stars">
          <span
            v-for="index in 5"
            :key="index"
            class="star"
            :class="{ filled: index <= starRating }"
            @click="setStarRating(index)"
          >
            ★
          </span>
        </div>
      </div>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      <button @click="submitReview">작성</button>
    </div>
    <p v-else-if="!isAuthenticated">로그인 후 리뷰를 작성할 수 있습니다.</p>

    <div v-if="reviews.length > 0">
      <ul>
        <li v-for="review in topReviews" :key="review.id">
          <router-link :to="{ name: 'ReviewDetail', params: { id: review.id } }">
            <strong>{{ review.title || "제목 없음" }}</strong>
          </router-link>
          - 좋아요: {{ review.like_count || 0 }}
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
      starRating: 0, // 별점
      errorMessage: "", // 에러 메시지
      movieAverageRating: 0, // 영화 평균 별점
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
      this.$router.go(-1);
    },
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
    goToMoviesByGenre(genreId) {
      this.$router.push({ name: "Movies", query: { genreId } });
    },
    fetchReviews(movieId) {
      axios
        .get(`/reviews/?movie_id=${movieId}`)
        .then((response) => {
          this.reviews = response.data.results || [];
          this.getTopReviews();
          this.calculateAverageRating();
        })
        .catch((error) => {
          console.error("리뷰 정보를 가져오는 중 오류 발생:", error);
        });
    },
    getTopReviews() {
      this.topReviews = this.reviews
        .sort((a, b) => {
          // 1. 평점 비교
          if (b.star_rating !== a.star_rating) {
            return b.star_rating - a.star_rating;
          }
          // 2. 좋아요 비교
          if (b.like_count !== a.like_count) {
            return b.like_count - a.like_count;
          }
          // 3. 최신순 비교
          return new Date(b.created_at) - new Date(a.created_at);
        })
        .slice(0, 3); // 상위 3개만 가져오기
    },
    toggleReviewForm() {
      this.showReviewForm = !this.showReviewForm;
      this.errorMessage = "";
    },
    validateReview() {
      if (!this.reviewTitle.trim()) {
        return "제목을 적어주세요.";
      }
      if (!this.reviewContent.trim()) {
        return "리뷰를 작성해주세요.";
      }
      if (this.starRating === 0) {
        return "평점을 입력해주세요.";
      }
      return null;
    },
    setStarRating(rating) {
      this.starRating = rating;
    },
    submitReview() {
      this.errorMessage = this.validateReview();
      if (this.errorMessage) {
        return;
      }

      const newReview = {
        movie_id: this.movie.id,
        title: this.reviewTitle.trim(),
        content: this.reviewContent.trim(),
        star_rating: this.starRating,
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
          this.starRating = 0;
          this.errorMessage = "";
          this.showReviewForm = false;
          this.fetchReviews(this.movie.id);
        })
        .catch((error) => {
          console.error(
            "리뷰 작성 중 오류 발생:",
            error.response?.data || error.message
          );
          alert("리뷰 작성에 실패했습니다.");
        });
    },
    calculateAverageRating() {
      if (this.reviews.length > 0) {
        const total = this.reviews.reduce(
          (sum, review) => sum + (review.star_rating || 0),
          0
        );
        this.movieAverageRating = (total / this.reviews.length).toFixed(1);
      } else {
        this.movieAverageRating = 0;
      }
    },
    getPosterPath(path) {
      return path
        ? `https://image.tmdb.org/t/p/w500${path}`
        : "https://via.placeholder.com/500x750?text=No+Image";
    },
    getStarRating(rating) {
      const filledStars = Math.floor(rating);
      const halfStar = rating % 1 >= 0.5 ? "★" : "";
      const emptyStars = 5 - filledStars - (halfStar ? 1 : 0);
      return "★".repeat(filledStars) + halfStar + "☆".repeat(emptyStars);
    },
  },
};
</script>

<style scoped>
.genres-container {
  display: flex; /* Flexbox로 한 줄 배치 */
  flex-wrap: nowrap; /* 줄바꿈 방지 */
  gap: 10px; /* 장르 간 간격 */
  margin-top: 10px; /* 위 내용과 간격 */
}

.clickable-genre {
  cursor: pointer;
  color: #007bff;
  text-decoration: underline;
}

.clickable-genre:hover {
  color: #0056b3;
}

/* 부모 컨테이너를 Flexbox로 설정 */
.movie-detail {
  display: flex;
  align-items: flex-start; /* 위쪽 정렬 */
  gap: 20px; /* 포스터와 정보 사이 간격 */
  margin-bottom: 20px;
}

/* 포스터 스타일 */
.poster img {
  max-width: 300px;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

/* 영화 정보 스타일 */
.info {
  flex: 1; /* 남은 공간을 차지 */
  display: flex;
  flex-direction: column;
  gap: 10px; /* 항목 간 간격 */
}

h1 {
  font-size: 24px;
  margin-bottom: 10px;
}

p {
  font-size: 16px;
  margin: 5px 0;
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

textarea {
  width: 100%;
  height: 120px;
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

input {
  width: 100%;
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

label {
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}

.error-message {
  color: red;
  font-size: 0.9rem;
  margin-bottom: 10px;
}

.rating {
  margin: 10px 0;
}

.stars {
  display: inline-block;
  cursor: pointer;
}

.star {
  font-size: 20px;
  color: gray;
}

.star.filled {
  color: gold;
}
</style>
