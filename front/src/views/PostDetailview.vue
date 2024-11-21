<template>
    <div class="post-detail">
      <h1>{{ post.title }}</h1>
      <p>작성자: {{ post.author }}</p>
      <p>작성일: {{ formatDate(post.created_at) }}</p>
      <p>좋아요: {{ post.likes }} | 싫어요: {{ post.dislikes }}</p>
      <p>{{ post.content }}</p>
      <comment-list :postId="post.id" />
    </div>
  </template>
  
  <script>
  import axios from "axios";
  import CommentList from "./CommentList.vue";
  
  export default {
    name: "PostDetailView",
    components: { CommentList },
    data() {
      return {
        post: null,
      };
    },
    methods: {
      fetchPost() {
        axios
          .get(`/api/posts/${this.$route.params.id}/`)
          .then((response) => {
            this.post = response.data;
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
      this.fetchPost();
    },
  };
  </script>
  
  <style scoped>
  .post-detail {
    margin: 20px;
  }
  </style>
  