<template>
    <div>
      <h1>글 작성</h1>
      <form @submit.prevent="submitPost">
        <label for="title">제목</label>
        <input v-model="title" id="title" required />
        <label for="content">내용</label>
        <textarea v-model="content" id="content" required></textarea>
        <label for="category">카테고리</label>
        <select v-model="category" id="category">
          <option value="공지사항">공지사항</option>
          <option value="영화토론방">영화토론방</option>
          <option value="영화수다방">영화수다방</option>
          <option value="잡담방">잡담방</option>
        </select>
        <button type="submit">작성</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    name: "PostForm",
    data() {
      return {
        title: "",
        content: "",
        category: "공지사항",
      };
    },
    methods: {
      submitPost() {
        axios
          .post("/api/posts/", {
            title: this.title,
            content: this.content,
            category: this.category,
          })
          .then(() => {
            alert("작성되었습니다!");
            this.$router.push({ name: "Community" });
          })
          .catch((error) => {
            console.error(error);
          });
      },
    },
  };
  </script>
  
  <style scoped>
  form {
    margin: 20px;
  }
  </style>
  