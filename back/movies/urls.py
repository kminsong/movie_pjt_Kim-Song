from django.urls import path
from .views import MovieList, MovieCreate

urlpatterns = [
    path('movies/', MovieList.as_view(), name='movie-list'),  # 영화 목록 조회 (GET)
    path('movies/create/', MovieCreate.as_view(), name='movie-create'),  # 영화 추가 (POST)
]
