<template>
  <div>
    <ul>
      <li v-for="comment in comments" :key="comment.id">
        <strong>{{ comment.author_name }}</strong>: {{ comment.content }}
        <span class="timestamp">{{ formatDate(comment.created_at) }}</span>
        <!-- 본인 댓글에만 수정/삭제 버튼 표시 -->
        <div v-if="comment.author_id === currentUserId" class="actions">
          <button @click="editComment(comment.id)">[수정]</button>
          <button @click="deleteComment(comment.id)">[삭제]</button>
        </div>
      </li>
    </ul>
    <form @submit.prevent="submitComment">
      <textarea v-model="content" placeholder="댓글을 입력하세요" required></textarea>
      <button type="submit">작성</button>
    </form>
  </div>
</template>

<script>
import axios from "@/api/axios";

export default {
  name: "CommentList",
  props: ["postId"],
  data() {
    return {
      comments: [], // 댓글 목록
      content: "", // 작성 중인 댓글 내용
      currentUserId: null, // 현재 로그인한 사용자 ID
    };
  },
  methods: {
    async fetchComments() {
      try {
        const response = await axios.get(`/community/posts/${this.postId}/comments/`);
        console.log("Fetched comments:", response.data);
        this.comments = response.data;
      } catch (error) {
        console.error("댓글 불러오기 실패:", error);
      }
    },
    async fetchCurrentUser() {
      try {
        const response = await axios.get("/accounts/profile/", {
          headers: { Authorization: `Token ${localStorage.getItem("authToken")}` },
        });
        this.currentUserId = response.data.id; // 현재 사용자 ID 저장
      } catch (error) {
        console.error("현재 사용자 정보를 가져오는 중 오류 발생:", error);
      }
    },
    async submitComment() {
      try {
        console.log("Submitting comment:", {
          post: this.postId,
          content: this.content,
          author: this.currentUserId,
        });
        await axios.post(
          `/community/posts/${this.postId}/comments/`,
          { post: this.postId, content: this.content },
          {
            headers: { Authorization: `Token ${localStorage.getItem("authToken")}` },
          }
        );
        this.content = ""; // 입력 필드 초기화
        this.fetchComments(); // 댓글 목록 갱신
      } catch (error) {
        console.error(
          "댓글 작성 실패:",
          error.response ? error.response.data : error
        );
      }
    },
    async editComment(commentId) {
      const newContent = prompt(
        "댓글 내용을 수정하세요:",
        this.comments.find(c => c.id === commentId).content
      );

      if (newContent) {
        try {
          const url = `/community/posts/${this.postId}/comments/${commentId}/`;
          console.log("Updating comment at:", url); // 디버깅: 요청 URL 확인
          console.log("Request data:", { content: newContent }); // 디버깅: 요청 데이터 확인

          await axios.patch(
            url, // PATCH 요청으로 변경
            { content: newContent }, // 수정 필드만 포함
            {
              headers: { Authorization: `Token ${localStorage.getItem("authToken")}` },
            }
          );

          this.fetchComments(); // 댓글 목록 갱신
          alert("댓글이 수정되었습니다.");
        } catch (error) {
          console.error("댓글 수정 실패:", error.response ? error.response.data : error);
          alert("댓글 수정에 실패했습니다.");
        }
      }
    },
    async deleteComment(commentId) {
      if (confirm("댓글을 삭제하시겠습니까?")) {
        try {
          await axios.delete(`/community/posts/${this.postId}/comments/${commentId}/`, {
            headers: { Authorization: `Token ${localStorage.getItem("authToken")}` },
          });
          this.fetchComments(); // 댓글 목록 갱신
        } catch (error) {
          console.error("댓글 삭제 실패:", error);
        }
      }
    },
    formatDate(dateString) {
      const options = {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
      };
      return new Date(dateString).toLocaleString(undefined, options);
    },
  },
  async created() {
    await this.fetchCurrentUser(); // 현재 로그인한 사용자 정보 가져오기
    this.fetchComments(); // 댓글 목록 가져오기
  },
};
</script>

<style scoped>
ul {
  list-style: none;
  padding: 0;
}
li {
  margin-bottom: 10px;
}
.timestamp {
  font-size: 0.8em;
  color: #888;
}
textarea {
  width: 100%;
  margin-bottom: 10px;
}
button {
  background-color: #007bff;
  color: white;
  padding: 5px 10px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
.actions {
  margin-left: 10px;
}
.actions button {
  background: none;
  color: #007bff;
  font-size: 0.9em;
  padding: 0;
  margin-left: 5px;
  border: none;
  cursor: pointer;
}
.actions button:hover {
  color: #0056b3;
  text-decoration: underline;
}
</style>
