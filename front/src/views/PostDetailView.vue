<template>
  <div>
    <h1 v-if="!editMode">{{ post.title }}</h1>
    <div v-else>
      <input v-model="editedPost.title" placeholder="제목을 입력하세요" />
    </div>

    <p><strong>작성자:</strong> {{ post.author_name }}</p>

    <div v-if="!editMode">
      <p><strong>내용:</strong> {{ post.content }}</p>
    </div>
    <div v-else>
      <textarea v-model="editedPost.content" placeholder="내용을 입력하세요"></textarea>
    </div>

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

    <!-- 수정/삭제 버튼 -->
    <div v-if="post.author_id === currentUserId" class="post-actions">
      <button v-if="!editMode" @click="enableEditMode">[수정]</button>
      <button v-else @click="saveChanges">[저장]</button>
      <button v-if="!editMode" @click="deletePost">[삭제]</button>
      <button v-else @click="cancelEditMode">[취소]</button>
    </div>

    <!-- 댓글 컴포넌트 -->
    <CommentList v-if="post.id" :postId="post.id" />
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
      editedPost: {}, // 수정 시 사용될 데이터
      editMode: false, // 수정 모드 상태
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
        this.editedPost = { ...response.data }; // 수정 시 사용할 데이터 초기화

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
    enableEditMode() {
      this.editMode = true;
    },
    async saveChanges() {
      try {
        await axios.put(
          `/community/posts/${this.post.id}/`,
          this.editedPost,
          {
            headers: { Authorization: `Token ${localStorage.getItem("authToken")}` },
          }
        );
        this.editMode = false; // 수정 모드 종료
        this.fetchPost(this.post.id); // 데이터 새로고침
        alert("게시글이 수정되었습니다.");
      } catch (error) {
        console.error("게시글 수정 실패:", error);
        alert("게시글 수정에 실패했습니다.");
      }
    },
    cancelEditMode() {
      this.editMode = false;
      this.editedPost = { ...this.post }; // 수정 데이터를 초기화
    },
    async deletePost() {
      if (confirm("정말로 게시글을 삭제하시겠습니까?")) {
        try {
          await axios.delete(`/community/posts/${this.post.id}/`, {
            headers: { Authorization: `Token ${localStorage.getItem("authToken")}` },
          });
          alert("게시글이 삭제되었습니다.");
          this.$router.push("/community"); // 삭제 후 커뮤니티 목록 페이지로 이동
        } catch (error) {
          console.error("게시글 삭제 실패:", error);
          alert("게시글 삭제에 실패했습니다.");
        }
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

.post-actions {
  margin: 10px 0;
}

button {
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

button:hover {
  opacity: 0.8;
}

textarea,
input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  font-size: 16px;
}
</style>
