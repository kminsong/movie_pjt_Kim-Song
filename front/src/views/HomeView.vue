<template>
  <div>
    <h1>랜덤 인기 영화</h1>
    <div class="movie-slider" ref="slider">
      <div class="movie-card" v-for="movie in movies" :key="movie.id">
        <img :src="getImageUrl(movie.poster_path)" :alt="movie.title" />
        <p>{{ movie.title }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import tmdb from '@/api/tmdb';

export default {
  data() {
    return {
      movies: [], // 영화 목록
    };
  },
  async created() {
    try {
      const randomPage = Math.floor(Math.random() * 500) + 1;

      // TMDB API 호출
      const response = await tmdb.get('/movie/popular', {
        params: {
          language: 'ko-KR',
          page: randomPage,
          include_adult: false, // 기본적으로 19금 콘텐츠 제외
        },
      });

      // API 응답 데이터를 movies에 저장
      this.movies = response.data.results;
    } catch (error) {
      console.error('Error fetching movies:', error.message);
    }
  },
  methods: {
    // 포스터 URL 생성
    getImageUrl(path) {
      return path
        ? `https://image.tmdb.org/t/p/w500${path}`
        : 'https://via.placeholder.com/150';
    },
  },
};
</script>

<style scoped>
.movie-slider {
  display: flex;
  gap: 10px;
  overflow-x: scroll;
  padding: 10px 0;
  scroll-behavior: smooth;
}

.movie-card {
  flex-shrink: 0;
  width: 150px;
  text-align: center;
}

.movie-card img {
  width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.movie-card p {
  margin-top: 10px;
  font-size: 0.9rem;
  font-weight: bold;
}
</style>
