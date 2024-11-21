<template>
    <div class="post-list">
      <h1>{{ category }}</h1>
      <div class="filters">
        <button @click="filterBy('latest')">전체글</button>
        <button @click="filterBy('hot')">Hot</button>
      </div>
      <div class="post-table">
        <div class="post-header">
          <span>제목</span>
          <span>작성자</span>
          <span>댓글 수</span>
          <span>좋아요 수</span>
          <span>작성 날짜</span>
        </div>
        <ul>
          <li
            v-for="post in posts"
            :key="post.id"
            :class="{ hot: post.is_hot }"
            @click="goToPostDetail(post.id)"
          >
            <span>{{ post.title }}</span>
            <span>{{ post.author }}</span>
            <span>{{ post.comment_count }}</span>
            <span>{{ post.likes }}</span>
            <span>{{ formatDate(post.created_at) }}</span>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    name: "PostList",
    props: ["category"],
    data() {
      return {
        posts: [],
        filter: "latest",
      };
    },
    methods: {
      fetchPosts() {
        axios
          .get(`/api/posts/?category=${this.category}&filter=${this.filter}`)
          .then((response) => {
            this.posts = response.data;
          })
          .catch((error) => {
            console.error(error);
          });
      },
      filterBy(filter) {
        this.filter = filter;
        this.fetchPosts();
      },
      goToPostDetail(postId) {
        this.$router.push({ name: "PostDetail", params: { id: postId } });
      },
      formatDate(date) {
        return new Date(date).toLocaleString();
      },
    },
    created() {
      this.fetchPosts();
    },
  };
  </script>
  
  <style scoped>
  .post-list {
    margin: 20px;
  }
  
  .filters button {
    margin: 5px;
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
    border-radius: 5px;
  }
  
  .filters button:hover {
    background-color: #0056b3;
  }
  
  .post-table {
    margin-top: 20px;
  }
  
  .post-header,
  ul li {
    display: flex;
    justify-content: space-between;
    padding: 10px;
    border-bottom: 1px solid #ddd;
  }
  
  ul li.hot span:first-child {
    color: blue;
  }
  </style>
  