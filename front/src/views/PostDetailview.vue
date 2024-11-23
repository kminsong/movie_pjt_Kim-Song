<template>
  <div>
    <h1>{{ post.title }}</h1>
    <p><strong>작성자:</strong> {{ post.author_name }}</p>
    <p><strong>내용:</strong> {{ post.content }}</p>
    <p>좋아요: {{ post.likes }} | 싫어요: {{ post.dislikes }}</p>

    <!-- 좋아요/싫어요 버튼 -->
    <div class="like-dislike-buttons">
      <p v-if="post.author_id === currentUserId">본인이 작성한 글입니다.</p>
      <div v-else>
        <button
          v-if="isAuthenticated"
          :class="{ liked: likedByUser }"
          @click="toggleLike"
        >
          <i :class="likedByUser ? 'fas fa-heart' : 'far fa-heart'"></i>
          {{ likedByUser ? "좋아요 취소" : "좋아요" }}
        </button>
        <button
          v-if="isAuthenticated"
          :class="{ disliked: dislikedByUser }"
          @click="toggleDislike"
        >
          <i :class="dislikedByUser ? 'fas fa-heart-broken' : 'far fa-heart-broken'"></i>
          {{ dislikedByUser ? "싫어요 취소" : "싫어요" }}
        </button>
        <p v-else>로그인 후 좋아요/싫어요를 누를 수 있습니다.</p>
      </div>
    </div>

    <!-- 댓글 컴포넌트 -->
    <CommentList :postId="post.id" />
  </div>
</template>

<script>
import axios from "@/api/axios";
import CommentList from "@/views/CommentList.vue";

export default {
  components: { CommentList },
  data() {
    return {
      post: {},
      isAuthenticated: false,
      likedByUser: false,
      dislikedByUser: false,
      currentUserId: null, // 현재 사용자 ID
    };
  },
  async created() {
    const postId = this.$route.params.id;

    this.isAuthenticated = !!localStorage.getItem("authToken");
    if (this.isAuthenticated) {
      await this.fetchCurrentUser();
    }

    await this.fetchPost(postId);
  },
  methods: {
    async fetchPost(postId) {
      try {
        const response = await axios.get(`/community/posts/${postId}/`, {
          headers: { Authorization: `Token ${localStorage.getItem("authToken")}` },
        });
        this.post = response.data;

        // 좋아요/싫어요 상태 설정
        this.likedByUser = response.data.liked_by_user || false;
        this.dislikedByUser = response.data.disliked_by_user || false;
      } catch (error) {
        console.error("게시글 정보를 가져오는 중 오류 발생:", error);
      }
    },
    async fetchCurrentUser() {
      try {
        const response = await axios.get("/accounts/profile/", {
          headers: { Authorization: `Token ${localStorage.getItem("authToken")}` },
        });
        this.currentUserId = response.data.id; // 사용자 ID 저장
      } catch (error) {
        console.error("현재 사용자 정보를 가져오는 중 오류 발생:", error);
      }
    },
    async toggleLike() {
      try {
        const response = await axios.post(
          `/community/posts/${this.post.id}/like/`,
          null,
          { headers: { Authorization: `Token ${localStorage.getItem("authToken")}` } }
        );
        this.post.likes = response.data.likes;
        this.likedByUser = !this.likedByUser; // 좋아요 상태 반전
      } catch (error) {
        console.error("좋아요 실패:", error);
      }
    },
    async toggleDislike() {
      try {
        const response = await axios.post(
          `/community/posts/${this.post.id}/dislike/`,
          null,
          { headers: { Authorization: `Token ${localStorage.getItem("authToken")}` } }
        );
        this.post.dislikes = response.data.dislikes;
        this.dislikedByUser = !this.dislikedByUser; // 싫어요 상태 반전
      } catch (error) {
        console.error("싫어요 실패:", error);
      }
    },
  },
};
</script>

<style scoped>
.like-dislike-buttons {
  display: flex;
  gap: 10px;
  margin: 10px 0;
}

button {
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

button.liked {
  background-color: #ff4d4d;
  color: white;
}

button.liked i {
  color: white;
}

button.disliked {
  background-color: #4d4dff;
  color: white;
}

button.disliked i {
  color: white;
}

button:hover {
  opacity: 0.8;
}

button i {
  margin-right: 5px;
  font-size: 20px;
}
</style>
