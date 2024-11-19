from django.db import models
from movies.models import Movie
from django.conf import settings  # AUTH_USER_MODEL 사용

class Review(models.Model):
    movie = models.ForeignKey(Movie, related_name="reviews", on_delete=models.CASCADE)  # 영화와 연결
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="reviews", on_delete=models.CASCADE)  # 작성자와 연결
    title = models.CharField(max_length=255)  # 리뷰 제목
    content = models.TextField()  # 리뷰 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일
    updated_at = models.DateTimeField(auto_now=True)  # 수정일
    like_count = models.PositiveIntegerField(default=0)  # 좋아요 수

    def __str__(self):
        return self.title
