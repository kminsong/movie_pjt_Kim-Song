from django.urls import path
from .views import ReviewList, ReviewCreate, TopReviewsForMovie

urlpatterns = [
    path('', ReviewList.as_view(), name='review-list'),
    path('create/', ReviewCreate.as_view(), name='review-create'),
    path('<int:movie_id>/top-reviews/', TopReviewsForMovie.as_view(), name='top-reviews'),  # 영화별 상위 리뷰
]
