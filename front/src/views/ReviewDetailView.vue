<template>
  <div>
    <h1>{{ review.title }}</h1>
    <!-- 영화 제목 -->
    <p class="movie-title">
      영화: 
      <router-link :to="{ name: 'MovieDetail', params: { id: review.movie_tmdb_id } }">
        {{ review.movie_title }}
      </router-link>
    </p>
    <p><strong>작성자:</strong> {{ review.user_nickname }}</p>
    <p v-if="!isEditing"><strong>내용:</strong> {{ review.content }}</p>

    <!-- 수정 폼 -->
    <div v-else>
      <input v-model="editedTitle" placeholder="수정할 제목을 입력하세요" />
      <textarea v-model="editedContent" placeholder="수정할 내용을 입력하세요"></textarea>
      <button @click="saveChanges">저장</button>
      <button @click="cancelEdit">취소</button>
    </div>

    <!-- 본인 작성 글에 대한 수정/삭제 링크 -->
    <div v-if="review.user_id === currentUserId" class="edit-delete-links">
      <span v-if="!isEditing" @click="startEdit" class="link">[수정]</span>
      <span v-if="!isEditing" class="spacer"></span>
      <span v-if="!isEditing" @click="confirmDelete" class="link">[삭제]</span>
    </div>

    <!-- 좋아요 -->
    <p v-if="!isEditing" class="likes">
      좋아요: {{ review.like_count }}
    </p>
    <!-- 좋아요 버튼 -->
    <button
      v-if="isAuthenticated && review.user_id !== currentUserId"
      :class="{ liked: likedByUser }"
      @click="toggleLike"
    >
      {{ likedByUser ? "좋아요 취소" : "좋아요" }}
    </button>
    <p v-else-if="review.user_id === currentUserId && !isEditing">
      본인이 작성한 글입니다.
    </p>
    <p v-else-if="!isAuthenticated">로그인 후 좋아요를 누를 수 있습니다.</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      review: {}, // 리뷰 데이터
      likedByUser: false, // 좋아요 상태
      isAuthenticated: false, // 로그인 여부
      currentUserId: null, // 현재 사용자 ID
      isEditing: false, // 수정 중 여부
      editedTitle: "", // 수정된 제목
      editedContent: "", // 수정된 내용
    };
  },
  async created() {
    const reviewId = this.$route.params.id;

    // 로그인 상태 확인
    this.isAuthenticated = !!localStorage.getItem("authToken");
    if (this.isAuthenticated) {
      await this.fetchCurrentUser();
    }

    // 리뷰 데이터 가져오기
    await this.fetchReviewDetail(reviewId);
  },
  methods: {
    async fetchReviewDetail(reviewId) {
      try {
        const response = await axios.get(`/reviews/${reviewId}/`, {
          headers: {
            Authorization: `Token ${localStorage.getItem("authToken")}`,
          },
        });
        this.review = response.data;
        this.likedByUser = response.data.liked_by_user; // 서버에서 받은 liked_by_user 상태
      } catch (error) {
        console.error("리뷰 상세 정보를 가져오는 중 오류 발생:", error);
      }
    },
    async fetchCurrentUser() {
      try {
        const response = await axios.get("/accounts/me/", {
          headers: { Authorization: `Token ${localStorage.getItem("authToken")}` },
        });
        this.currentUserId = response.data.id;
      } catch (error) {
        console.error("현재 사용자 정보를 가져오는 중 오류 발생:", error);
      }
    },
    toggleLike() {
      axios
        .post(`/reviews/${this.review.id}/like/`, null, {
          headers: { Authorization: `Token ${localStorage.getItem("authToken")}` },
        })
        .then((response) => {
          this.review.like_count = response.data.like_count;
          this.likedByUser = !this.likedByUser; // 좋아요 상태 반전
        })
        .catch((error) => {
          console.error("좋아요 추가/취소 중 오류 발생:", error);
        });
    },
    startEdit() {
      this.isEditing = true;
      this.editedTitle = this.review.title;
      this.editedContent = this.review.content;
    },
    cancelEdit() {
      this.isEditing = false;
    },
    async saveChanges() {
      try {
        const response = await axios.put(
          `/reviews/${this.review.id}/`,
          {
            title: this.editedTitle.trim(),
            content: this.editedContent.trim(),
            movie_id: this.review.movie_id, // movie_id 추가
          },
          {
            headers: { Authorization: `Token ${localStorage.getItem("authToken")}` },
          }
        );
        this.review.title = response.data.title;
        this.review.content = response.data.content;
        this.isEditing = false;
        alert("수정되었습니다!");
      } catch (error) {
        console.error("리뷰 수정 중 오류 발생:", error);
        alert("수정에 실패했습니다.");
      }
    },
    async confirmDelete() {
      if (!confirm("삭제하시겠습니까?")) {
        return; // 취소를 누르면 아무것도 하지 않음
      }
      try {
        await axios.delete(`/reviews/${this.review.id}/`, {
          headers: { Authorization: `Token ${localStorage.getItem("authToken")}` },
        });
        alert("삭제되었습니다!");
        this.$router.push("/reviews");
      } catch (error) {
        console.error("리뷰 삭제 중 오류 발생:", error);
        alert("삭제에 실패했습니다.");
      }
    },
  },
};
</script>

<style scoped>
button {
  padding: 5px 10px;
  border: none;
  color: white;
  background-color: #007bff;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

button.liked {
  background-color: #ff4d4d;
}

button.liked:hover {
  background-color: #ff1a1a;
}

textarea,
input {
  width: 100%;
  margin-bottom: 10px;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

textarea {
  height: 80px;
}

.movie-title {
  font-size: 18px;
  margin-bottom: 10px;
}

.likes {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
}

.edit-delete-links {
  margin-top: 10px;
}

.link {
  color: #007bff;
  cursor: pointer;
  text-decoration: underline;
}

.link:hover {
  color: #0056b3;
}

.spacer {
  display: inline-block;
  width: 20px;
}
</style>
