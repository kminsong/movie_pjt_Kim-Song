<template>
    <div class="modal-overlay">
      <div class="modal-content">
        <h3>선호 장르 선택</h3>
        <div class="genres">
          <button
            v-for="genre in genres"
            :key="genre.id"
            :class="{ selected: selectedGenres.includes(genre.id) }"
            @click="toggleGenre(genre.id)"
          >
            {{ genre.name }}
          </button>
        </div>
        <div class="actions">
          <button @click="$emit('close')">취소</button>
          <button :disabled="selectedGenres.length !== 3" @click="save">
            확인
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import tmdb from "@/api/tmdb";
  
  export default {
    props: {
      selectedGenres: {
        type: Array,
        required: true,
      },
    },
    data() {
      return {
        genres: [], // TMDB에서 가져온 장르 목록
      };
    },
    created() {
      this.fetchGenres();
    },
    methods: {
      async fetchGenres() {
        try {
          const response = await tmdb.get("/genre/movie/list", {
            params: { language: "ko-KR" },
          });
          this.genres = response.data.genres; // TMDB 응답 데이터를 장르로 설정
        } catch (error) {
          console.error("장르 데이터를 가져오는 중 오류 발생:", error);
        }
      },
      toggleGenre(genreId) {
        if (this.selectedGenres.includes(genreId)) {
          this.$emit(
            "update:selectedGenres",
            this.selectedGenres.filter((id) => id !== genreId)
          );
        } else if (this.selectedGenres.length < 3) {
          this.$emit("update:selectedGenres", [...this.selectedGenres, genreId]);
        }
      },
      save() {
        console.log("저장할 장르 ID:", this.selectedGenres); // 디버깅 로그 추가
        this.$emit("save", this.selectedGenres);
      },
    },
  };
  </script>
  
  <style scoped>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .modal-content {
    background: white;
    padding: 20px;
    border-radius: 8px;
    text-align: center;
    width: 300px;
  }
  
  .genres {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 10px;
    margin-bottom: 20px;
  }
  
  button {
    padding: 10px 20px;
    cursor: pointer;
  }
  
  button.selected {
    background-color: #007bff;
    color: white;
  }
  
  .actions button {
    margin: 10px;
  }
  </style>