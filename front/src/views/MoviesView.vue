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

    <!-- 페이지네이션 -->
    <div v-if="totalPages > 1" class="pagination">
      <button :disabled="currentPage === 1" @click="changePage(1)">처음</button>
      <button :disabled="currentPage === 1" @click="changePage(currentPage - 1)">
        이전
      </button>
      <button
        v-for="page in visiblePages"
        :key="page"
        :class="{ active: currentPage === page }"
        @click="changePage(page)"
      >
        {{ page }}
      </button>
      <button
        :disabled="currentPage === totalPages"
        @click="changePage(currentPage + 1)"
      >
        다음
      </button>
      <button
        :disabled="currentPage === totalPages"
        @click="changePage(totalPages)"
      >
        마지막
      </button>
    </div>
  </div>
</template>

<script>
import tmdb from "@/api/tmdb";

export default {
  data() {
    return {
      genres: [],
      selectedGenres: [],
      orderBy: "popularity",
      searchQuery: "",
      movies: [],
      currentPage: 1,
      totalPages: 0,
    };
  },
  computed: {
    visiblePages() {
      const range = 4; // 현재 페이지 기준 앞뒤로 보여줄 페이지 수
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
    this.fetchGenres();
    this.searchMovies();
  },
  methods: {
    fetchGenres() {
      tmdb
        .get("/genre/movie/list", { params: { language: "ko-KR" } })
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
      this.selectedGenres = [];
      this.searchMovies();
    },
    setOrderBy(order) {
      this.orderBy = order;
      this.searchMovies();
    },
    searchMovies() {
      const params = {
        language: "ko-KR",
        sort_by:
          this.orderBy === "popularity"
            ? "popularity.desc"
            : this.orderBy === "release_date"
            ? "release_date.desc"
            : "vote_average.desc",
        page: this.currentPage,
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
          this.movies = response.data.results || [];
          this.totalPages = response.data.total_pages || 0;
        })
        .catch((error) => {
          console.error("영화 데이터를 가져오는 중 오류 발생:", error);
          this.movies = [];
        });
    },
    changePage(page) {
      this.currentPage = page;
      this.searchMovies();
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
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
}

.movie-item {
  text-align: center;
  cursor: pointer;
}

.movie-item img {
  width: 100%;
  max-width: 150px;
  height: auto;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 10px;
}

.pagination button {
  width: 40px; /* 고정된 버튼 크기 */
  height: 40px; /* 고정된 버튼 높이 */
  padding: 0;
  border: none;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  text-align: center;
  font-size: 14px;
}

.pagination button.active {
  background-color: #0056b3;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
