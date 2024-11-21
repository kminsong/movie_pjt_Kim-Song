from django.urls import path
from .views import (
    ReviewListCreate,
    TopReviewsForMovie,
    ReviewDetailAPIView,
    LikeReview,  # 추가
)

urlpatterns = [
    path("", ReviewListCreate.as_view(), name="review-list-create"),  # 리뷰 목록 및 생성
    path("<int:movie_id>/top-reviews/", TopReviewsForMovie.as_view(), name="top-reviews"),  # 영화의 인기 리뷰
    path("<int:pk>/", ReviewDetailAPIView.as_view(), name="review-detail"),  # 단일 리뷰 조회
    path("<int:review_id>/like/", LikeReview.as_view(), name="review-like"),  # 좋아요 추가 엔드포인트
]
