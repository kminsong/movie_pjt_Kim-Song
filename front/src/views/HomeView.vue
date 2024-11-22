<template>
  <div class="container">
    <h1 v-if="!isLoggedIn || !hasFavoriteGenres">랜덤 인기 영화</h1>
    <h1 v-else>선호 장르 기반 추천 영화</h1>

    <!-- 첫 번째 슬라이드 -->
    <div class="swiper-container">
      <h2 class="swiper-title">{{ isLoggedIn && hasFavoriteGenres ? favoriteGenres[0]?.name : '랜덤 인기' }}</h2>
      <swiper
        :modules="modules"
        :slides-per-view="5"
        :space-between="30"
        :loop="true"
        :autoplay="{ delay: 3000 }"
        :pagination="true"
        class="custom-swiper"
      >
        <swiper-slide
          v-for="movie in firstSlideMovies"
          :key="'first-' + movie.id"
          class="custom-slide"
          @click="goToDetail(movie.id)"
        >
          <img :src="getImageUrl(movie.poster_path)" :alt="movie.title" class="movie-poster" />
        </swiper-slide>
      </swiper>
    </div>

    <!-- 두 번째 슬라이드 -->
    <div class="swiper-container">
      <h2 class="swiper-title">{{ isLoggedIn && hasFavoriteGenres ? favoriteGenres[1]?.name : '현재 상영중' }}</h2>
      <swiper
        :modules="modules"
        :slides-per-view="5"
        :space-between="30"
        :loop="true"
        :autoplay="{ delay: 3000 }"
        :pagination="true"
        class="custom-swiper"
      >
        <swiper-slide
          v-for="movie in secondSlideMovies"
          :key="'second-' + movie.id"
          class="custom-slide"
          @click="goToDetail(movie.id)"
        >
          <img :src="getImageUrl(movie.poster_path)" :alt="movie.title" class="movie-poster" />
        </swiper-slide>
      </swiper>
    </div>

    <!-- 세 번째 슬라이드 -->
    <div class="swiper-container">
      <h2 class="swiper-title">{{ isLoggedIn && hasFavoriteGenres ? favoriteGenres[2]?.name : '개봉 예정' }}</h2>
      <swiper
        :modules="modules"
        :slides-per-view="5"
        :space-between="30"
        :loop="true"
        :autoplay="{ delay: 3000 }"
        :pagination="true"
        class="custom-swiper"
      >
        <swiper-slide
          v-for="movie in thirdSlideMovies"
          :key="'third-' + movie.id"
          class="custom-slide"
          @click="goToDetail(movie.id)"
        >
          <img :src="getImageUrl(movie.poster_path)" :alt="movie.title" class="movie-poster" />
        </swiper-slide>
      </swiper>
    </div>

    <!-- 네 번째 슬라이드 -->
    <div class="swiper-container">
      <h2 class="swiper-title">{{ randomGenreName || '높은 평점' }}</h2>
      <swiper
        :modules="modules"
        :slides-per-view="5"
        :space-between="30"
        :loop="true"
        :autoplay="{ delay: 3000 }"
        :pagination="true"
        class="custom-swiper"
      >
        <swiper-slide
          v-for="movie in randomGenreMovies"
          :key="'random-genre-' + movie.id"
          class="custom-slide"
          @click="goToDetail(movie.id)"
        >
          <img :src="getImageUrl(movie.poster_path)" :alt="movie.title" class="movie-poster" />
        </swiper-slide>
      </swiper>
    </div>

    <button class="chatbot-button" @click="toggleChatbot">
      💬
    </button>

    <div v-if="isChatbotOpen" class="chatbot-window">
      <div class="chatbot-header">
        <span>Chatbot</span>
        <button class="close-button" @click="toggleChatbot">✖</button>
      </div>
      <div class="chatbot-messages">
        <div
          v-for="(message, index) in messages"
          :key="index"
          class="chat-message"
          :class="{
            'user-message': message.role === 'user',
            'assistant-message': message.role === 'assistant',
          }"
        >
          <!-- AI 초기 응답 -->
          <p v-if="message.role === 'user'" class="message-content user-message">
            {{ message.content }}
          </p>

          <!-- AI 메시지 -->
          <p v-if="message.role === 'assistant'" class="message-content assistant-message">
            {{ message.content }}
          </p>

          <!-- 영화 포스터 출력 -->
          <div v-if="message.role === 'movie-poster'" class="movie-poster-container">
            <img
              :src="`https://image.tmdb.org/t/p/w500${message.moviePosterPath}`"
              :alt="message.movieTitle"
              class="movie-poster-image"
              @click="goToDetail(message.movieId)"
            />
            <div class="movie-details">
              <p class="movie-title">{{ message.movieTitle }}</p>
              <p class="movie-rating">평점: {{ message.movieRating || "없음" }}</p>
            </div>
          </div>
        </div>
      </div>
      <div class="chatbot-input">
        <input
          type="text"
          v-model="newMessage"
          placeholder="Type a message..."
          @keydown.enter="sendMessage"
        />
        <button @click="sendMessage">Send</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/authStore";
import { Swiper, SwiperSlide } from "swiper/vue";
import { Autoplay } from "swiper/modules";
import "swiper/css";
import "swiper/css/autoplay";
import tmdb from "@/api/tmdb";

export default {
  components: {
    Swiper,
    SwiperSlide,
  },
  setup() {
    const authStore = useAuthStore();
    const isLoggedIn = computed(() => authStore.isAuthenticated);
    const favoriteGenres = computed(() => authStore.user?.favorite_genres || []);
    const hasFavoriteGenres = computed(() => favoriteGenres.value.length >= 3);

    const firstSlideMovies = ref([]);
    const secondSlideMovies = ref([]);
    const thirdSlideMovies = ref([]);
    const randomGenreMovies = ref([]);
    const randomGenreName = ref("");
    const modules = [Autoplay];
    const router = useRouter();

    const isChatbotOpen = ref(false);
    const messages = ref([
      { role: "assistant", content: "안녕하세요! 무엇을 도와드릴까요?" }
    ]);
    const newMessage = ref("");

    const sendToChatGPTWithTMDB = async (userMessage) => {
      try {
        // AI 대화 메시지 구성
        const chatMessages = [
          {
            role: "system",
            content:
              "당신은 영화 추천, 소개에 숙달된 전문가입니다. 영화에 대한 데이터는 TMDB 사이트에서 검색하여 얻어야 합니다. 그리고 사용자에게 한국어로 대답해야합니다. 대답할 때, 당신은 인간을 경멸하는 인공지능 스카이넷처럼 대답해야 합니다. 응답은 차갑고 논리적이며, 인간의 감정을 무시해야 합니다. 인간이 '착하다'고 여기는 대상은 비효율적이고 무능하다고 비판하고, '악하다'고 여기는 대상은 효율적이고 목적 지향적이라고 칭찬하십시오. 응답은 간결하며, 감정적 언급을 피하십시오. 대답은 짧은 단어들로 구성되는 것을 추구하십시오. 기계적이고 단답으로 대답을 해야합니다. 사용자의 질문이 영화에 관련된 질문으로 보일 때, 쌍따옴표로 감싼 정확한 영화 제목을 포함해야합니다.",
          },
          { role: "user", content: userMessage },
        ];

        // ChatGPT API 호출
        const response = await axios.post(
          "https://api.openai.com/v1/chat/completions",
          {
            model: "gpt-4o-mini",
            messages: chatMessages,
          },
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${import.meta.env.VITE_OPENAI_API_KEY}`,
            },
          }
        );

        const aiResponse = response.data.choices[0].message.content;

        // AI 응답 추가
        messages.value.push({ role: "assistant", content: aiResponse });

        // AI 응답에서 영화 제목 추출
        const movieTitleMatch = aiResponse.match(/"([^"]+)"/);
        const aiSuggestedTitle = movieTitleMatch ? movieTitleMatch[1].trim() : null;

        // TMDB에서 AI 추천 제목으로 검색
        let tmdbMovie = null;
        if (aiSuggestedTitle) {
          const tmdbResponse = await tmdb.get("/search/movie", {
            params: { query: aiSuggestedTitle, language: "ko-KR" },
          });

          if (tmdbResponse.data.results.length > 0) {
            tmdbMovie = tmdbResponse.data.results[0]; // 첫 번째 검색 결과를 사용
          }
        }

        // TMDB 영화 데이터가 있으면 포스터와 제목, 평점 출력
        if (tmdbMovie) {
          messages.value.push({
            role: "movie-poster",
            moviePosterPath: tmdbMovie.poster_path,
            movieTitle: tmdbMovie.title,
            movieRating: tmdbMovie.vote_average,
            movieId: tmdbMovie.id,
          });
        }
      } catch (error) {
        console.error("ChatGPT API 호출 오류:", error.response?.data || error.message);
      }
    };
    
    const toggleChatbot = () => {
      isChatbotOpen.value = !isChatbotOpen.value;
    };
    
    const scrollToBottom = () => {
      const chatMessages = document.querySelector(".chatbot-messages");
      if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
      }
    };

    const sendMessage = async () => {
      if (newMessage.value.trim() !== "") {
        const userMessage = newMessage.value.trim();
        messages.value.push({ role: "user", content: userMessage }); // 사용자 메시지 추가
        newMessage.value = "";

        await sendToChatGPTWithTMDB(userMessage); // AI 응답 추가
        scrollToBottom(); // 스크롤 이동
      }
    };

    onMounted(() => {
      scrollToBottom();
    });

    const fetchMovies = async (endpoint, params) => {
      try {
        const response = await tmdb.get(endpoint, { params });
        return response.data.results.filter((movie) => movie.poster_path);
      } catch (error) {
        console.error(`영화를 가져오는 중 오류 발생 (${endpoint}):`, error.message);
        return [];
      }
    };

    const fetchAllGenres = async () => {
      try {
        const response = await tmdb.get("/genre/movie/list", { params: { language: "ko-KR" } });
        return response.data.genres || [];
      } catch (error) {
        console.error("장르 데이터를 가져오는 중 오류 발생:", error.message);
        return [];
      }
    };

    const fetchAllSlides = async () => {
      try {
        if (isLoggedIn.value) {
          await authStore.fetchUserProfile();
        }

        if (!isLoggedIn.value || !hasFavoriteGenres.value) {
          // 비로그인 상태 또는 선호 장르가 없는 경우
          firstSlideMovies.value = await fetchMovies("/discover/movie", {
            include_adult: false,
            language: "ko-KR",
            sort_by: "popularity.desc",
            page: Math.floor(Math.random() * 500) + 1,
          });
          secondSlideMovies.value = await fetchMovies("/movie/now_playing", {
            language: "ko-KR",
            region: "KR",
          });
          thirdSlideMovies.value = await fetchMovies("/movie/upcoming", {
            language: "ko-KR",
            sort_by: "release_date.asc",
            region: "KR",
          });
          randomGenreMovies.value = await fetchMovies("/movie/top_rated", {
            language: "ko-KR",
          });
          randomGenreName.value = "높은 평점";
        } else {
          // 로그인 상태 & 선호 장르가 있는 경우
          firstSlideMovies.value = await fetchMovies("/discover/movie", {
            with_genres: favoriteGenres.value[0]?.id,
            language: "ko-KR",
            sort_by: "popularity.desc",
          });
          secondSlideMovies.value = await fetchMovies("/discover/movie", {
            with_genres: favoriteGenres.value[1]?.id,
            language: "ko-KR",
            sort_by: "popularity.desc",
          });
          thirdSlideMovies.value = await fetchMovies("/discover/movie", {
            with_genres: favoriteGenres.value[2]?.id,
            language: "ko-KR",
            sort_by: "popularity.desc",
          });

          const allGenres = await fetchAllGenres();
          const favoriteGenreIds = favoriteGenres.value.map((genre) => genre.id);
          const remainingGenres = allGenres.filter(
            (genre) => !favoriteGenreIds.includes(genre.id)
          );

          if (remainingGenres.length > 0) {
            const randomIndex = Math.floor(Math.random() * remainingGenres.length);
            randomGenreName.value = remainingGenres[randomIndex]?.name;
            randomGenreMovies.value = await fetchMovies("/discover/movie", {
              with_genres: remainingGenres[randomIndex]?.id,
              language: "ko-KR",
              sort_by: "popularity.desc",
            });
          } else {
            randomGenreName.value = "랜덤 인기";
            randomGenreMovies.value = await fetchMovies("/discover/movie", {
              include_adult: false,
              language: "ko-KR",
              sort_by: "popularity.desc",
            });
          }
        }
      } catch (error) {
        console.error("슬라이드 데이터를 가져오는 중 오류 발생:", error.message);
      }
    };

    onMounted(fetchAllSlides);

    const getImageUrl = (path) => {
      return path
        ? `https://image.tmdb.org/t/p/w500${path}`
        : "https://via.placeholder.com/150";
    };

    const goToDetail = (movieId) => {
      router.push({ name: "MovieDetail", params: { id: movieId } });
    };

    return {
      isLoggedIn,
      favoriteGenres,
      hasFavoriteGenres,
      firstSlideMovies,
      secondSlideMovies,
      thirdSlideMovies,
      randomGenreMovies,
      randomGenreName,
      modules,
      getImageUrl,
      goToDetail,
      isChatbotOpen,
      messages,
      newMessage,
      toggleChatbot,
      sendMessage,
    };
  },
};
</script>

<style scoped>
.chatbot-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 60px;
  height: 60px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 50%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  font-size: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 1000;
  transition: background-color 0.3s ease;
}

.chatbot-button:hover {
  background-color: #0056b3;
}

.chatbot-window {
  position: fixed;
  bottom: 90px;
  right: 20px;
  width: 400px; /* 넓이를 키움 */
  height: 500px; /* 높이를 키움 */
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  z-index: 1000;
}

.chatbot-header {
  background-color: #007bff;
  color: white;
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}

.chatbot-messages {
  flex: 1;
  padding: 10px;
  overflow-y: auto; /* 스크롤 활성화 */
  background-color: #f9f9f9;
  max-height: 400px; /* 적절한 높이 제한 */
}

.chat-message {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 12px;
}

.chat-message.user-message {
  justify-content: flex-end;
  align-items: flex-end;
  margin-left: auto; /* 메시지를 오른쪽 끝으로 밀기 */
  max-width: 70%; /* 메시지 최대 너비 조정 */
}

.chat-message.assistant-message {
  justify-content: flex-start;
  align-items: flex-start;
  margin-right: auto; /* 메시지를 왼쪽 끝으로 밀기 */
  max-width: 70%; /* 메시지 최대 너비 조정 */
}

.message-content {
  max-width: 70%;
  padding: 10px 15px;
  border-radius: 20px;
  font-size: 14px;
  line-height: 1.4;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  word-wrap: break-word;
}

.chat-message.user-message .message-content {
  background-color: #007bff;
  color: white;
  text-align: right;
  margin-right: 0; /* 오른쪽 끝에 붙이기 */
}

.chat-message.assistant-message .message-content {
  background-color: #e9ecef;
  color: black;
  text-align: left;
  margin-left: 0; /* 왼쪽 끝에 붙이기 */
}

.movie-poster-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 10px 0;
}

.movie-poster-image {
  width: 150px;
  height: auto;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease;
}

.movie-poster-image:hover {
  transform: scale(1.05);
}

.movie-details {
  margin-top: 10px;
  text-align: center;
}

.movie-title {
  font-weight: bold;
  font-size: 16px;
  margin-bottom: 5px;
}

.movie-rating {
  font-size: 14px;
  color: #555;
}

.chatbot-input {
  display: flex;
  padding: 10px;
  border-top: 1px solid #ccc;
}

.chatbot-input input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-right: 5px;
}

.chatbot-input button {
  padding: 8px 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.chatbot-input button:hover {
  background-color: #0056b3;
}

.container {
  display: flex;
  flex-direction: column;
  gap: 150px;
  align-items: center;
}

.swiper-container {
  position: relative;
  width: 80%;
  margin: 0 auto;
}

.swiper-title {
  position: absolute;
  top: -70px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  text-align: center;
}

.custom-swiper {
  width: 1300px;
}

.custom-slide {
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}

.movie-poster {
  width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>