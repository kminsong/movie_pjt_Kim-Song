<template>
  <div>
    <ul>
      <li v-for="comment in comments" :key="comment.id">
        <strong>{{ comment.author_name }}</strong>: {{ comment.content }}
        <span class="timestamp">{{ formatDate(comment.created_at) }}</span>
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
      comments: [],
      content: "",
    };
  },
  methods: {
    async fetchComments() {
      try {
        const response = await axios.get(`/community/posts/${this.postId}/comments/`);
        this.comments = response.data;
      } catch (error) {
        console.error("댓글 불러오기 실패:", error);
      }
    },
    async submitComment() {
      try {
        console.log("Submitting comment:", {
          post: this.postId,
          content: this.content,
        }); // 디버깅: 요청 데이터 출력
        await axios.post(
          `/community/posts/${this.postId}/comments/`,
          { post: this.postId, content: this.content }, // post 필드 추가
          {
            headers: { Authorization: `Token ${localStorage.getItem("authToken")}` },
          }
        );
        this.content = "";
        this.fetchComments();
      } catch (error) {
        console.error(
          "댓글 작성 실패:",
          error.response ? error.response.data : error
        );
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
  created() {
    this.fetchComments();
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
}
</style>
