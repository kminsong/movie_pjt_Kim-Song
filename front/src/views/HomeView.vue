<template>
  <div>
    <h1>랜덤 인기 영화</h1>
    <swiper
      :modules="modules"
      :slides-per-view="3"
      :space-between="-50"
      :loop="true"
      :autoplay="{ delay: 3000 }"
      :effect="'coverflow'"
      :coverflow-effect="{
        rotate: 75,
        stretch: 20,
        depth: 100,
        modifier: 1,
        slideShadows: true
      }"
      :pagination="true"
      class="custom-swiper"
    >
      <swiper-slide
        v-for="movie in movies"
        :key="movie.id"
        class="custom-slide"
        @click="goToDetail(movie.id)"
      >
        <img :src="getImageUrl(movie.poster_path)" :alt="movie.title" class="movie-poster" />
      </swiper-slide>
    </swiper>
  </div>
</template>

<script>
import { ref } from "vue";
import { useRouter } from "vue-router";

// Swiper 모듈과 Vue 컴포넌트
import { Swiper, SwiperSlide } from "swiper/vue";
import { Autoplay, EffectCoverflow } from "swiper/modules";

// Swiper 스타일
import "swiper/css";
import "swiper/css/autoplay";
import "swiper/css/effect-coverflow";

import tmdb from "@/api/tmdb";

export default {
  components: {
    Swiper,
    SwiperSlide,
  },
  setup() {
    const movies = ref([]);
    const modules = [Autoplay, EffectCoverflow];
    const router = useRouter();

    const fetchMovies = async () => {
      try {
        const totalMovies = 20; // 가져올 총 영화 수
        const fetchedMovies = new Set();

        while (fetchedMovies.size < totalMovies) {
          const randomPage = Math.floor(Math.random() * 500) + 1;

          // TMDB API 호출 (include_adult=false로 성인 영화 필터링)
          const response = await tmdb.get("/discover/movie", {
            params: {
              include_adult: false, // 성인 영화 제외
              language: "ko-KR",
              page: randomPage,
              sort_by: "popularity.desc", // 인기순 정렬
            },
          });

          // 포스터 경로가 존재하는 영화만 필터링
          response.data.results
            .filter((movie) => movie.poster_path) // 포스터 경로가 있는 영화만 포함
            .forEach((movie) => fetchedMovies.add(JSON.stringify(movie)));
        }

        // Set에서 중복 제거 후 배열로 변환
        movies.value = Array.from(fetchedMovies)
          .map((movie) => JSON.parse(movie))
          .slice(0, totalMovies);
      } catch (error) {
        console.error("Error fetching movies:", error.message);
      }
    };

    fetchMovies();

    const getImageUrl = (path) => {
      return path
        ? `https://image.tmdb.org/t/p/w500${path}`
        : "https://via.placeholder.com/150";
    };

    const goToDetail = (movieId) => {
      router.push({ name: "MovieDetail", params: { id: movieId } });
    };

    return {
      movies,
      modules,
      getImageUrl,
      goToDetail,
    };
  },
};
</script>

<style scoped>
.custom-swiper {
  width: 500px;
  margin: 0 auto;
}

.custom-slide {
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer; /* 클릭 가능하도록 커서 변경 */
}

.movie-poster {
  width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
