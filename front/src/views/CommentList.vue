<template>
    <div>
      <h2>댓글</h2>
      <ul>
        <li v-for="comment in comments" :key="comment.id">
          <p>{{ comment.author }}: {{ comment.content }}</p>
          <p>작성일: {{ formatDate(comment.created_at) }}</p>
        </li>
      </ul>
      <form @submit.prevent="submitComment">
        <textarea v-model="newComment" placeholder="댓글 작성"></textarea>
        <button type="submit">댓글 작성</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    name: "CommentList",
    props: ["postId"],
    data() {
      return {
        comments: [],
        newComment: "",
      };
    },
    methods: {
      fetchComments() {
        axios
          .get(`/api/posts/${this.postId}/comments/`)
          .then((response) => {
            this.comments = response.data;
          })
          .catch((error) => {
            console.error(error);
          });
      },
      submitComment() {
        axios
          .post(`/api/posts/${this.postId}/comments/`, {
            content: this.newComment,
          })
          .then(() => {
            this.newComment = "";
            this.fetchComments();
          })
          .catch((error) => {
            console.error(error);
          });
      },
      formatDate(date) {
        return new Date(date).toLocaleString();
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
  
  form {
    margin-top: 20px;
  }
  </style>
  