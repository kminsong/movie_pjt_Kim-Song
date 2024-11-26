<template>
  <div class="review-detail">
    <!-- 포스터와 리뷰 정보를 flex 레이아웃으로 정렬 -->
    <div class="poster-and-info">
      <!-- 영화 포스터 -->
      <div v-if="review.movie_poster" class="poster">
        <img
          :src="'https://image.tmdb.org/t/p/w500' + review.movie_poster"
          alt="영화 포스터"
          class="movie-poster"
        />
      </div>

      <!-- 리뷰 정보 -->
      <div class="info">
        <!-- 제목 수정 필드 -->
        <h1 v-if="isEditing">
          <input v-model="editedTitle" placeholder="제목을 입력하세요" />
        </h1>
        <h1 v-else>{{ review.title }}</h1>

        <!-- 영화 제목 -->
        <p class="movie-title">
          영화: 
          <router-link :to="{ name: 'MovieDetail', params: { id: review.movie_tmdb_id } }">
            {{ review.movie_title }}
          </router-link>
        </p>

        <!-- 작성자 정보 -->
        <p><strong>작성자:</strong> {{ review.user_nickname }}</p>

        <!-- 본인이 준 별점 -->
        <p class="star-rating">
          <strong>내 별점:</strong>
          <span
            v-for="n in 5"
            :key="n"
            class="star"
            :class="{ filled: n <= (isEditing ? editedStarRating : review.star_rating) }"
            @click="isEditing && updateStarRating(n)"
          >
            ★
          </span>
        </p>

        <!-- 좋아요 -->
        <p class="likes">좋아요: {{ review.like_count }}</p>

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

        <!-- 수정/삭제 링크 -->
        <p v-if="review.user_id === currentUserId" class="edit-delete-links">
          <span v-if="!isEditing" @click="startEdit" class="link">[수정]</span>
          <span v-if="!isEditing" class="spacer"></span>
          <span v-if="!isEditing" @click="confirmDelete" class="link">[삭제]</span>
        </p>

        <!-- 저장/취소 버튼 -->
        <div v-if="isEditing" class="edit-actions">
          <span @click="saveChanges" class="link">[저장]</span>
          <span class="spacer"></span>
          <span @click="cancelEdit" class="link">[취소]</span>
        </div>
      </div>
    </div>

    <!-- 내용 수정 필드 -->
    <div class="review-box">
      <p v-if="!isEditing">{{ review.content }}</p>
      <textarea
        v-if="isEditing"
        v-model="editedContent"
        placeholder="내용을 입력하세요"
      ></textarea>
    </div>
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
      editedStarRating: 0, // 수정 중인 별점
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
        const headers = {};
        if (this.isAuthenticated) {
          headers.Authorization = `Token ${localStorage.getItem("authToken")}`;
        }

        const response = await axios.get(`/reviews/${reviewId}/`, { headers });
        this.review = response.data;
        this.editedStarRating = this.review.star_rating; // 초기 별점 설정
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
      this.editedStarRating = this.review.star_rating;
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
            star_rating: this.editedStarRating, // 수정된 별점 저장
            movie_id: this.review.movie_id, // movie_id 추가
          },
          {
            headers: { Authorization: `Token ${localStorage.getItem("authToken")}` },
          }
        );
        this.review.title = response.data.title;
        this.review.content = response.data.content;
        this.review.star_rating = response.data.star_rating; // 별점 업데이트
        this.isEditing = false;
        alert("수정되었습니다!");
      } catch (error) {
        console.error("리뷰 수정 중 오류 발생:", error);
        alert("수정에 실패했습니다.");
      }
    },
    async confirmDelete() {
      if (!confirm("삭제하시겠습니까?")) {
        return;
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
    updateStarRating(star) {
      this.editedStarRating = star; // 선택된 별점 저장
    },
  },
};
</script>

<style scoped>
.review-detail {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 70px;
}

.poster-and-info {
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

.poster {
  flex-shrink: 0;
}

.movie-poster {
  width: 200px;
  height: auto;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  margin-bottom: 20px;
}

.review-box {
  min-height: 7cm;
  width: 500px;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: left;
  margin-top: 20px;
}

.review-box p {
  margin: 0;
  font-size: 16px;
  color: #333;
}

textarea {
  width: 100%;
  height: 200px; /* 수정 시 높이 증가 */
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  resize: none;
}

input {
  height: 40px; /* 제목 수정 칸 높이 고정 */
  line-height: 40px;
  padding: 0 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

.star-rating {
  font-size: 18px;
  margin-top: 10px;
  color: #f39c12;
  cursor: pointer;
}

.star {
  font-size: 24px;
  color: #ddd;
}

.star.filled {
  color: #f39c12;
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