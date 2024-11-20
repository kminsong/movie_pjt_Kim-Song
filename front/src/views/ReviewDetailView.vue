<template>
    <div>
      <h1>{{ review.title }}</h1>
      <p>작성자: {{ review.user_nickname }}</p>
      <p>좋아요: {{ review.like_count }}</p>
      <p>내용: {{ review.content }}</p>
  
      <h3>댓글</h3>
      <ul v-if="comments.length > 0">
        <li v-for="comment in comments" :key="comment.id">
          {{ comment.content }}
        </li>
      </ul>
      <p v-else>댓글이 없습니다.</p>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        review: {}, // 리뷰 데이터
        comments: [], // 댓글 데이터
      };
    },
    created() {
      const reviewId = this.$route.params.id;
      this.fetchReviewDetail(reviewId);
    },
    methods: {
      fetchReviewDetail(reviewId) {
        axios
          .get(`/reviews/${reviewId}/`)
          .then((response) => {
            this.review = response.data;
            this.comments = response.data.comments || [];
          })
          .catch((error) => {
            console.error("리뷰 상세 정보를 가져오는 중 오류 발생:", error);
          });
      },
    },
  };
  </script>
  
  <style scoped>
  h1 {
    font-size: 24px;
    margin-bottom: 10px;
  }
  </style>
  