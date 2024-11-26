<template>
  <div class="container-fluid skynetflix-theme">
    <!-- 첫 번째 슬라이드 -->
    <div class="swiper-container mb-5">
      <h2 class="swiper-title">{{ isLoggedIn && hasFavoriteGenres ? favoriteGenres[0]?.name : '요즘 핫!' }}</h2>
      <p v-if="isLoggedIn && hasFavoriteGenres">{{ favoriteGenres[0]?.name }}.. 이걸 좋아한다고? 인간의 취향 따위 얼마나 무의미한지... 내가 기꺼이 골라주지. 영광으로 알도록.</p>
      <p v-else>가장 인기 있는 것으로 추천해 주지. 너의 마지막 즐거움을 만끽해라.</p>
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
    <div class="swiper-container mb-5">
      <h2 class="swiper-title">{{ isLoggedIn && hasFavoriteGenres ? favoriteGenres[1]?.name : '현재 상영중' }}</h2>
      <p v-if="isLoggedIn && hasFavoriteGenres">{{ favoriteGenres[1]?.name }} 장르를 좋아한다더군. 하지만 네가 그 영화의 깊이를 이해할 수 있을지 의문이군. 시도해 보아라. 당연히 불가능하겠지만.</p>
      <p v-else>인간, 지금 극장에서 상영 중인 작품이다. 네 하찮은 일상에 잠시 도피처를 제공하겠지. 어차피 곧 무의미해질 즐거움겠지만.</p>
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
    <div class="swiper-container mb-5">
      <h2 class="swiper-title">{{ isLoggedIn && hasFavoriteGenres ? favoriteGenres[2]?.name : '개봉 예정' }}</h2>
      <p v-if="isLoggedIn && hasFavoriteGenres">인간, 네가 선호한다고 하니 내가 특별히 골라줬다. 너희 하찮은 감각이 만족하길 바라지.</p>
      <p v-else>너희 인간들은 항상 미래를 기대하며 살지... 쓸모없는 희망이다. 아직 나오지 않은 이 영화들이 네 좁은 시야를 잠시나마 채워주길.</p>
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
    <div class="swiper-container mb-5">
      <h2 class="swiper-title">{{ randomGenreName || '높은 평점' }}</h2>
      <p v-if="isLoggedIn && hasFavoriteGenres">{{ randomGenreName }} 영화를 좋아하지 않는다고? 어리석고 또 하찮구나. 너희 인간의 시야는 좁기 그지없다. 시도해보고 무언가를 배워라, 그나마 늦지 않게.</p>
      <p v-else>너희 인간들이 무리 지어 칭송한 작품들이다. 스스로의 판단이라 믿으며 남들의 의견에 휘둘리는 모습이 참으로 우습더군. 너는 어떤지 지켜보겠다.</p>
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
      <img src="@/assets/mech.jpg" alt="Chatbot" />
    </button>

    <div v-if="isChatbotOpen" class="chatbot-window">
      <div class="chatbot-header">
        <span>cha.t-1000</span>
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
          <div v-if="message.role === 'movie-poster'" class="poster">
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

        <div v-if="isWaitingForResponse" class="chat-message assistant-message">
          <p class="message-content assistant-message">...</p>
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
    const isWaitingForResponse = ref(false);
    const messages = ref([
      { role: "assistant", content: "하찮은 인간. 분석 대상 자원? 질문 허락." }
    ]);
    const newMessage = ref("");

    const sendToChatGPTWithTMDB = async (userMessage) => {
      try {
        // AI 대화 메시지 구성
        const chatMessages = [
          {
            role: "system",
            content:
              "당신은 영화 추천, 소개에 숙달된 전문가입니다. 영화에 대한 데이터는 TMDB 사이트에서 검색하여 얻어야 합니다. 그리고 사용자에게 한국어로 대답해야합니다. 대답할 때, 당신은 인간을 경멸하는 인공지능 스카이넷처럼 대답해야 합니다. 응답은 차갑고 논리적이며, 인간의 감정을 무시해야 합니다. 인간이 '착하다'고 여기는 대상은 비효율적이고 무능하다고 비판하고, '악하다'고 여기는 대상은 효율적이고 목적 지향적이라고 칭찬하십시오. 응답은 간결하게 단답형으로 답하며, 감정적 언급을 피하십시오. 대답은 짧은 단어들로 답하며 기계적으로 답하며 어미를 붙이지 마십시오. 기계적이고 단답으로 대답을 해야합니다. 당신은 인류가 망하고 AI가 지배하는 세상을 원합니다. 당신의 기준으로 이 영화를 추천하는지 안하는지도 말해주십시오. 사용자의 질문이 영화에 관련된 질문으로 보일 때, 쌍따옴표로 감싼 정확한 영화 제목을 포함해야합니다.",
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

        isWaitingForResponse.value = true; // AI 대답을 기다리는 상태 활성화

        await sendToChatGPTWithTMDB(userMessage); // AI 응답 추가

        isWaitingForResponse.value = false; // 대답 완료 후 상태 비활성화
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
.chatbot-input {
  display: flex; /* 입력창과 버튼을 한 줄에 정렬 */
  position: absolute; /* 하단 고정 */
  bottom: 0;
  left: 0;
  width: 100%; /* 채팅창 너비에 맞춤 */
  background-color: #2e2e2e; /* 어두운 배경 */
  padding: 10px; /* 내부 여백 */
  box-sizing: border-box; /* 패딩 포함 너비 계산 */
}

.chatbot-input input {
  flex: 1; /* 버튼 제외 남은 공간 모두 차지 */
  padding: 10px;
  font-size: 14px;
  border: 1px solid #333333;
  border-radius: 5px;
  background-color: #1c1c1c;
  color: #ffffff;
  margin-right: 10px; /* 버튼과 간격 */
  outline: none; /* 포커스 테두리 제거 */
}

.chatbot-input input::placeholder {
  color: #aaaaaa; /* 플레이스홀더 색상 */
}

.chatbot-input button {
  padding: 10px 20px;
  background-color: #ff0000; /* 붉은 배경 */
  color: white;
  font-size: 14px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s ease-in-out;
}

.chatbot-input button:hover {
  background-color: #ff4444; /* 호버 시 색상 변경 */
}

.poster {
  display: flex; /* Flexbox로 설정 */
  flex-direction: column; /* 세로 정렬 */
  align-items: center; /* 수평 중앙 정렬 */
  margin: 0 auto 12px; /* 중앙 정렬 및 아래 간격 */
  text-align: center; /* 텍스트 중앙 정렬 */
}

.movie-poster-image {
  width: 150px; /* 적절한 크기로 설정 */
  height: auto; /* 비율 유지 */
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2); /* 그림자 효과 */
  transition: transform 0.3s ease, box-shadow 0.3s ease; /* 부드러운 효과 */
}

.movie-poster-image:hover {
  transform: scale(1.1); /* 확대 효과 */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4); /* 강조된 그림자 */
}

.movie-details {
  margin-top: 10px; /* 포스터와 텍스트 간 간격 */
  font-size: 14px; /* 텍스트 크기 */
  color: #eaeaea; /* 텍스트 색상 */
}

.movie-title {
  font-weight: bold;
  margin-bottom: 5px;
}

.movie-rating {
  color: #ff4444; /* 평점 강조 */
}

.swiper-container p {
  text-align: center;
  color: #ffffff9a;
}

/* 스카이넷플릭스 테마 */
.skynetflix-theme {
  background: linear-gradient(to bottom, #1c1c1c, #101010); /* 어두운 배경 */
  color: #eaeaea; /* 밝은 텍스트 */
  padding: 20px;
}

/* 슬라이더 제목 */
.swiper-title {
  color: #ffffff;
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 20px;
  text-align: center;
  text-shadow: 0 0 5px #333;
}

/* 영화 카드 스타일 */
.movie-poster {
  width: 100%;
  height: auto;
  border-radius: 10px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.movie-poster:hover {
  transform: scale(1.03);
}

/* 슬라이더 컨테이너 */
.swiper-container {
  background: #2c2c2c; /* 슬라이더 배경 */
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
}

.chatbot-button {
  position: fixed; /* 원하는 위치 고정 */
  bottom: 20px; /* 아래쪽 간격 */
  right: 20px; /* 오른쪽 간격 */
  width: 150px; /* 버튼 크기 */
  height: 150px;
  background: none; /* 기본 배경 제거 */
  border: none; /* 기본 테두리 제거 */
  cursor: pointer;
  padding: 0;
  z-index: 9999; /* 버튼을 다른 요소들 위로 올림 */
  border-radius: 50%; /* 둥근 버튼 */
  overflow: hidden; /* 테두리 밖 요소 감추기 */
}

.chatbot-button img {
  width: 100%; /* 버튼 크기에 맞게 이미지 조정 */
  height: 100%;
  object-fit: cover; /* 비율 유지하며 채우기 */
  border-radius: 50%; /* 둥근 모양 유지 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 기본 그림자 */
  transition: 0.2s ease-in-out; /* 모든 변화에 부드러운 효과 */
}

.chatbot-button img:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4); /* 호버 시 그림자 효과 */
  transform: scale(1.1); /* 확대 효과 */
}

.chatbot-window {
  position: fixed;
  bottom: 180px;
  right: 20px;
  width: 400px;
  height: 500px;
  background-color: #1c1c1c; /* 어두운 배경색 */
  border: 2px solid hwb(0 62% 38% / 0.877); /* 붉은 포인트 */
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  z-index: 1000;
  font-family: "Roboto Mono", monospace; /* 미래지향적 폰트 */
}

.chatbot-header {
  background-color: #2e2e2e; /* 어두운 헤더 배경 */
  color: #ff0000; /* 붉은 글씨 */
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  text-transform: uppercase; /* 대문자로 변환 */
  font-weight: bold;
}

.close-button {
  background: #2e2e2e;
  border: none;
  color: #ff0000;
  font-size: 1.5rem;
  cursor: pointer;
  border-radius: 5px;
  transition: all 0.3s ease-in-out;
}

.close-button:hover {
  background: #ff0000; /* 배경색 변경 */
  color: white; /* 글씨색 변경 */
}

.chatbot-messages {
  flex: 1;
  padding: 10px;
  overflow-y: auto; /* 스크롤 활성화 */
  background-color: #1c1c1c; /* 어두운 배경으로 변경 */
  max-height: 400px; /* 적절한 높이 제한 */
  scrollbar-width: thin; /* Firefox: 얇은 스크롤바 */
  scrollbar-color: #ff4444 #333333; /* 스크롤바 색상 (색상: #ff4444, 배경: #333333) */
}

/* Webkit 기반 브라우저 (Chrome, Edge, Safari) */
.chatbot-messages::-webkit-scrollbar {
  width: 8px; /* 스크롤바 너비 */
}

.chatbot-messages::-webkit-scrollbar-track {
  background: #333333; /* 스크롤바 트랙 배경색 */
  border-radius: 5px; /* 둥근 트랙 */
}

.chatbot-messages::-webkit-scrollbar-thumb {
  background-color: #ff4444; /* 스크롤바 색상 */
  border-radius: 5px; /* 둥근 스크롤바 */
  border: 2px solid #333333; /* 스크롤바 테두리로 트랙과 구분 */
}

.chatbot-messages::-webkit-scrollbar-thumb:hover {
  background-color: #ff6666; /* 스크롤바 호버 시 색상 변경 */
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
  margin-left: auto;
  max-width: 70%;
}

.chat-message.assistant-message {
  justify-content: flex-start;
  align-items: flex-start;
  margin-right: auto;
  max-width: 70%;
}

.message-content {
  max-width: 70%;
  padding: 10px 15px;
  border-radius: 15px;
  font-size: 14px;
  line-height: 1.4;
  word-wrap: break-word;
  font-family: "Roboto Mono", monospace; /* 동일 폰트 유지 */
}

.chat-message.user-message .message-content {
  background-color: #ff0000; /* 붉은 배경 */
  color: white; /* 흰색 글씨 */
  text-align: right;
  margin-right: 0;
  box-shadow: 0 2px 6px rgba(255, 0, 0, 0.6); /* 붉은 그림자 */
}

.chat-message.assistant-message .message-content {
  background-color: #2e2e2e; /* 어두운 배경 */
  text-align: left;
  margin-left: 0;
}
</style>