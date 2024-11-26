<template>
  <div class="bg">
    <div v-if="trailerUrl" class="trailer-container">
      <iframe
        :src="trailerUrl"
        allowfullscreen
        title="Movie Trailer"
      ></iframe>
    </div>
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
          <button
            v-for="genre in movie?.genres"
            :key="genre.id"
            @click="goToMoviesByGenre(genre.id)"
            class="genre-button"
          >
            #{{ genre.name }}
          </button>
        </div>
      </div>
    </div>

    <div class="review-container">
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
        <button @click="submitReview" class="create_bt">작성</button>
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
    </div>

    <div class="similar-movies-container" v-if="similarMovies.length > 0">
      <h3>비슷한 영화 추천</h3>
      <h6>그 영화가 마음에 든다면, 이런 영화도 좋아하겠군.</h6>
      <div class="similar-movies">
        <div
          v-for="movie in similarMovies"
          :key="movie.id"
          class="similar-movie-card"
          @click="goToMovieDetail(movie.id)"
        >
          <img :src="getPosterPath(movie.poster_path)" :alt="movie.title" />
          <p>{{ truncateText(movie.title, 20) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import tmdb from "@/api/tmdb";
import axios from "axios";

export default {
  data() {
    return {
      movie: null, // 현재 영화 데이터
      trailerUrl: null, // 트레일러 URL 추가
      reviews: [], // 전체 리뷰 목록
      topReviews: [], // 상위 3개 리뷰
      similarMovies: [],
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
      this.fetchMovieTrailer(movieId); // 트레일러 가져오기
      this.fetchReviews(movieId); // 영화 리뷰 가져오기
      this.fetchSimilarMovies(movieId);
    } else {
      console.error("영화 ID가 유효하지 않습니다.");
    }

    this.isAuthenticated = !!localStorage.getItem("authToken"); // 토큰으로 로그인 상태 확인
  },
  methods: {
    truncateText(text, maxLength) {
      if (!text) return ''; // text가 undefined인 경우 처리
      return text.length > maxLength ? `${text.slice(0, maxLength)}...` : text;
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
    fetchMovieTrailer(movieId) {
      // 1. 한국어 트레일러 시도
      tmdb
        .get(`/movie/${movieId}/videos`, { params: { language: "ko-KR" } })
        .then((response) => {
          const trailers = response.data.results.filter(
            (video) => video.type === "Trailer" && video.site === "YouTube"
          );

          if (trailers.length > 0) {
            // 한국어 트레일러가 있으면 설정
            this.trailerUrl = `https://www.youtube.com/embed/${trailers[0].key}`;
          } else {
            // 2. 영어 트레일러 요청
            this.fetchEnglishTrailer(movieId);
          }
        })
        .catch((error) => {
          console.error("트레일러 정보를 가져오는 중 오류 발생:", error);
          // 한국어 트레일러 요청 실패 시 영어 트레일러 시도
          this.fetchEnglishTrailer(movieId);
        });
    },

    // 영어 트레일러를 가져오는 메서드 추가
    fetchEnglishTrailer(movieId) {
      tmdb
        .get(`/movie/${movieId}/videos`, { params: { language: "en-US" } })
        .then((response) => {
          const trailers = response.data.results.filter(
            (video) => video.type === "Trailer" && video.site === "YouTube"
          );

          if (trailers.length > 0) {
            this.trailerUrl = `https://www.youtube.com/embed/${trailers[0].key}`;
          } else {
            console.warn("트레일러가 없습니다.");
          }
        })
        .catch((error) => {
          console.error("영어 트레일러 정보를 가져오는 중 오류 발생:", error);
        });
    },
    fetchSimilarMovies(movieId) {
      tmdb
        .get(`/movie/${movieId}/similar`, { params: { language: "ko-KR" } })
        .then((response) => {
          this.similarMovies = response.data.results || [];
          console.log("Similar Movies:", this.similarMovies); // 디버깅용
        })
        .catch((error) => {
          console.error("비슷한 영화를 가져오는 중 오류 발생:", error);
        });
    },
    goToMovieDetail(movieId) {
      console.log(`Navigating to movie detail with ID: ${movieId}`);
      this.$router.push({ name: "MovieDetail", params: { id: movieId } })
        .catch((err) => {
          console.error("Router navigation error:", err);
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
      console.log(newReview)
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
  watch: {
    '$route.params.id': {
      immediate: true,
      handler(newId) {
        this.fetchMovieDetails(newId);
        this.fetchMovieTrailer(newId);
        this.fetchReviews(newId);
        this.fetchSimilarMovies(newId);
      },
    },
  },
};
</script>

<style scoped>
.similar-movies-container {
  margin: 20px 100px;
  background: #2c2c2c;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
}

.similar-movies {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: flex-start;
}

.similar-movie-card {
  width: 150px;
  cursor: pointer;
  text-align: center;
}

.similar-movie-card img {
  width: 100%;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.similar-movie-card p {
  margin-top: 10px;
  font-size: 14px;
  color: #eaeaea;
}

.create_bt {
  margin-right: 105px;
}

h1 {
  font-size: 42px !important; /* 강제 적용 */
  font-weight: bold;
}

.bg {
  min-height: 100vh; /* 화면 전체 높이를 최소 높이로 설정 */
  display: flex; /* 중앙 정렬을 위한 Flexbox */
  flex-direction: column; /* 세로 정렬 */
}

.review-container {
  position: relative;
  align-items: flex-start;
  margin: 20px 100px; /* 무비 디테일 컨테이너와 간격 */
  background: #2c2c2c;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
}

.review-container button {
  position: absolute; /* 버튼을 절대 위치로 설정 */
  top: 15px; /* 컨테이너 위에서 10px */
  right: 15px; /* 컨테이너 오른쪽에서 10px */
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 5px;
  cursor: pointer;
}

.review-container button:hover {
  background-color: #0056b3; /* 버튼 hover 스타일 */
}

.trailer-container {
  min-width: 500px;
  position: relative;
  width: 60%; /* 너비: 화면의 80% */
  margin: 40px auto 10px; /* 상하 여백을 각각 10px로 설정 */
  padding-bottom: 30%; /* 높이를 16:9 비율보다 작게 (45%로 설정) */
  overflow: hidden;
  border-radius: 10px; /* 선택 사항: 모서리를 둥글게 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5); /* 선택 사항: 그림자 */
  background-color: #000; /* 비디오 로드 전 배경 */
}

.trailer-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%; /* 부모 컨테이너 너비에 맞춤 */
  height: 100%; /* 부모 컨테이너 높이에 맞춤 */
  border: 0;
}

.genres-container {
  display: flex;
  flex-wrap: wrap; /* 버튼을 여러 줄로 배치 */
  gap: 10px; /* 버튼 간 간격 */
  margin-top: 10px;
}

.genre-button {
  background-color: #007bff; /* 버튼 배경색 */
  color: white; /* 버튼 텍스트 색상 */
  border: none; /* 기본 테두리 제거 */
  border-radius: 20px; /* 둥근 모양 */
  padding: 8px 15px; /* 버튼 안쪽 여백 */
  font-size: 14px; /* 글씨 크기 */
  cursor: pointer; /* 마우스 커서를 포인터로 */
  transition: background-color 0.3s ease; /* 호버 애니메이션 */
}

.genre-button:hover {
  background-color: #0056b3; /* 호버 시 배경색 */
}

.genre-button:active {
  background-color: #003f7f; /* 클릭 시 배경색 */
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
  min-width: 600px;
  display: flex;
  gap: 30px;
  align-items: flex-start; /* 위쪽 정렬 */
  margin: 20px 100px;
  background: #2c2c2c;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
}
.swiper-container {
  background: #2c2c2c; /* 슬라이더 배경 */
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
}
/* 포스터 스타일 */
.poster img {
  min-width: 250px;
  width: 250px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

/* 영화 정보 스타일 */
.info {
  display: flex;
  flex-direction: column;
  gap: 15px; /* 항목 간 간격 */
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

.similar-movies-container h6 {
  color: #c9c9c9b9;
  margin-bottom: 20px;
}
</style>
