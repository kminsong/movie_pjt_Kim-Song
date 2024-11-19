<template>
  <div>
    <h1>영화 탐색</h1>
    <div>
      <h3>영화 검색</h3>
      <input v-model="searchQuery" placeholder="영화 이름을 입력하세요" />
    </div>

    <div>
      <h3>장르 선택</h3>
      <div class="genres">
        <!-- 전체 장르 박스 -->
        <button
          :class="{ selected: selectedGenres.length === 0 }"
          @click="clearGenres"
        >
          전체
        </button>
        <button
          v-for="genre in genres"
          :key="genre.id"
          :class="{ selected: selectedGenres.includes(genre.id) }"
          @click="toggleGenre(genre.id)"
        >
          {{ genre.name }}
        </button>
      </div>
    </div>

    <div>
      <h3>정렬</h3>
      <button @click="setOrderBy('popularity')">인기순</button>
      <button @click="setOrderBy('release_date')">최신순</button>
      <button @click="setOrderBy('vote_average')">평점순</button>
    </div>

    <div>
      <button @click="searchMovies">검색</button>
    </div>

    <div>
      <h3>영화 목록</h3>
      <div v-if="movies && movies.length > 0" class="movie-list">
        <div
          v-for="movie in movies"
          :key="movie.id"
          class="movie-item"
          @click="goToDetail(movie.id)"
        >
          <img :src="getPosterPath(movie.poster_path)" alt="poster" />
          <p>{{ movie.title || '제목 없음' }}</p>
        </div>
      </div>
      <p v-else>해당되는 영화가 없습니다</p>
    </div>
  </div>
</template>

<script>
import tmdb from "@/api/tmdb";

export default {
  data() {
    return {
      genres: [], // 장르 목록
      selectedGenres: [], // 선택된 장르 (초기 상태: 전체 선택)
      orderBy: "popularity", // 기본 정렬: 인기순
      searchQuery: "", // 검색어
      movies: [], // 영화 목록
    };
  },
  created() {
    this.fetchGenres();
    this.searchMovies(); // 컴포넌트 생성 시 전체 영화 목록 표시
  },
  methods: {
    fetchGenres() {
      tmdb
        .get("/genre/movie/list", { params: { language: "ko-KR" } }) // 한국어로 요청
        .then((response) => {
          this.genres = response.data.genres;
        })
        .catch((error) => {
          console.error("장르 데이터를 가져오는 중 오류 발생:", error);
        });
    },
    toggleGenre(genreId) {
      if (this.selectedGenres.includes(genreId)) {
        this.selectedGenres = this.selectedGenres.filter((id) => id !== genreId);
      } else {
        this.selectedGenres.push(genreId);
      }
    },
    clearGenres() {
      this.selectedGenres = []; // 선택된 장르 초기화
      this.searchMovies(); // 전체 영화 다시 검색
    },
    setOrderBy(order) {
      this.orderBy = order;
      this.searchMovies(); // 정렬 기준 변경 시 즉시 검색
    },
    searchMovies() {
      const params = {
        language: "ko-KR", // 한국어 요청
        sort_by: this.orderBy === "popularity"
          ? "popularity.desc"
          : this.orderBy === "release_date"
          ? "release_date.desc"
          : "vote_average.desc", // 평점순 정렬
      };

      if (this.selectedGenres.length > 0) {
        params.with_genres = this.selectedGenres.join(",");
      }

      if (this.searchQuery) {
        params.query = this.searchQuery;
      }

      const apiEndpoint = this.searchQuery ? "/search/movie" : "/discover/movie";

      tmdb
        .get(apiEndpoint, { params })
        .then((response) => {
          console.log("API 응답 데이터:", response.data.results); // 응답 데이터 확인
          this.movies = response.data.results || [];
        })
        .catch((error) => {
          console.error("영화 데이터를 가져오는 중 오류 발생:", error);
          this.movies = [];
        });
    },
    goToDetail(movieId) {
      this.$router.push({ name: "MovieDetail", params: { id: movieId } });
    },
    getPosterPath(path) {
      return path
        ? `https://image.tmdb.org/t/p/w500${path}`
        : "https://via.placeholder.com/500x750?text=No+Image";
    },
  },
};
</script>

<style>
.genres button {
  margin: 5px;
  padding: 10px;
  border: 1px solid #ccc;
  background-color: white;
  cursor: pointer;
}

.genres button.selected {
  background-color: #007bff;
  color: white;
}

.movie-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.movie-item {
  text-align: center;
  cursor: pointer;
}

.movie-item img {
  width: 200px;
  height: auto;
}
</style>
