<template>
  <div>
    <h1>글 작성</h1>
    <form @submit.prevent="submitPost">
      <label for="title">제목</label>
      <input v-model="title" id="title" required />

      <label for="content">내용</label>
      <textarea v-model="content" id="content" required></textarea>

      <button type="submit">작성</button>
    </form>
  </div>
</template>

<script>
import api from "@/api/axios";

export default {
  name: "PostForm",
  data() {
    return {
      title: "",
      content: "",
    };
  },
  methods: {
    async submitPost() {
      try {
        // API 요청 보내기
        await api.post("/community/posts/", {
          title: this.title,
          content: this.content,
        });
        alert("작성되었습니다!");
        this.$router.push({ name: "Community" });
      } catch (error) {
        console.error("작성 중 오류 발생:", error);
        alert("작성에 실패했습니다. 다시 시도해주세요.");
      }
    },
  },
};
</script>


<style scoped>
form {
  margin: 20px;
}

label {
  display: block;
  margin: 10px 0 5px;
  font-weight: bold;
}

input,
textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

textarea {
  height: calc(5 * 40px);
  resize: vertical;
}

button {
  padding: 10px 15px;
  border: none;
  background-color: #007bff;
  color: white;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
