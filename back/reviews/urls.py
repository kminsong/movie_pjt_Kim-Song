from django.urls import path
from .views import ReviewListCreate, TopReviewsForMovie, ReviewDetailAPIView

urlpatterns = [
    path('', ReviewListCreate.as_view(), name='review-list-create'),  # 리뷰 목록 및 생성
    path('<int:movie_id>/top-reviews/', TopReviewsForMovie.as_view(), name='top-reviews'),  # 영화의 인기 리뷰
    path('<int:pk>/', ReviewDetailAPIView.as_view(), name='review-detail'),  # 단일 리뷰 조회
]
