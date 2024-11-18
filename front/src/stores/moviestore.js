import { defineStore } from "pinia";
import axios from "axios";

export const useMovieStore = defineStore("movieStore", {
  state: () => ({
    movies: [], // 영화 데이터를 저장하는 상태
  }),

  actions: {
    async fetchMovies() {
      try {
        const response = await axios.get("http://localhost:8000/movies/");
        this.movies = response.data;
      } catch (error) {
        console.error("Failed to fetch movies:", error.message);
      }
    },
  },
});
