<template>
  <div>
    <div class="filter container">
      <h1 class="title">영화 탐색</h1>
      <div class="search-container">
        <input v-model="searchQuery" placeholder="영화 이름을 입력하세요" @keyup.enter="searchMovies" />
        <button class="search-button" @click="searchMovies">검색</button>
      </div>

      <div class="filter-options">
        <div>
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
          <div class="sort-buttons">
            <button @click="setOrderBy('popularity')">인기순</button>
            <button @click="setOrderBy('release_date')">최신순</button>
            <button @click="setOrderBy('vote_average')">평점순</button>
          </div>
        </div>
      </div>
    </div>
    <div class="movie-list container">
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
        <div v-if="movies.length === 20" class="circle-placeholder">
          <img src="@/assets/skynetflix.jpg" alt="Skynetflix Logo" class="center-logo" />
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
    const genreId = this.$route.query.genreId;
    if (genreId) {
      this.selectedGenres = [parseInt(genreId)];
    }
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
.circle-placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 220px; /* 원하는 높이 설정 */
}

.center-logo {
  width: 170px; /* 로고 크기 */
  height: 170px;
  border-radius: 50%; /* 동그라미 모양 */
  object-fit: cover; /* 비율 유지하며 잘리지 않게 표시 */
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.5); /* 그림자 효과 */
}

.circle-placeholder::after {
  font-size: 2rem;
  color: white;
  font-weight: bold;
}


.container {
  min-width: 600px;
  background: #2c2c2c;
  margin: 30px;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
}

.title {
  text-align: center;
  font-size: 2rem;
  color: #fff;
  margin-bottom: 20px;
}

.search-container {
  display: flex; /* 버튼과 입력창을 한 줄에 배치 */
  align-items: center; /* 세로 중앙 정렬 */
  justify-content: center; /* 양쪽 요소를 가운데 정렬 */
  gap: 10px; /* 입력창과 버튼 간격 */
  margin-bottom: 20px;
}

.search-container input {
  width: 70%; /* 입력창 너비 */
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.filter-options {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
}

.genres {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.genres button {
  padding: 10px;
  border: 1px solid #ccc;
  background-color: white;
  cursor: pointer;
  border-radius: 15px; /* 모서리를 둥글게 설정 */
  transition: background-color 0.3s ease, color 0.3s ease; /* 호버 시 부드러운 전환 효과 */
}

.genres button.selected {
  background-color: #007bff;
  color: white;
  border-radius: 15px; /* selected 버튼도 동일한 둥글기 적용 */
}

.genres button:hover {
  background-color: #f0f0f0; /* 호버 시 밝은 배경색 */
}


.sort-buttons button {
  margin: 5px;
  padding: 10px;
  border: 1px solid #ccc;
  background-color: white;
  cursor: pointer;
}

.search-button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s ease-in-out;
}

.search-button:hover {
  background-color: #0056b3;
}

.movie-list.container {
  width: 90%; /* 너비를 화면의 90%로 설정 */
  margin: 20px auto; /* 좌우 균등하게 중앙 정렬 */
  padding: 20px;
  background: #2c2c2c;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
}

.movie-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); /* 열 자동 조정 */
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
  margin-bottom: 10px; /* 포스터와 제목 사이의 간격 추가 */
}

.pagination {
  margin-top: 20px;
  margin-bottom: 40px; /* 하단 간격 추가 */
  display: flex;
  justify-content: center;
  gap: 20px;
}

.pagination button {
  width: 50px; /* 고정된 버튼 크기 */
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

html {
  background-color: #101010; /* 영화 페이지와 동일한 어두운 배경색 */
  margin: 0; /* 여백 제거 */
  padding: 0; /* 여백 제거 */
}
</style>
