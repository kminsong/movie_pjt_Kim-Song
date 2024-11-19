from django.contrib.auth.models import AbstractUser
from django.db import models
from movies.models import Genre  # 좋아하는 장르 연결을 위해 import

class User(AbstractUser):
    """
    커스텀 유저 모델
    """
    nickname = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(unique=True, null=False)
    favorite_genres = models.ManyToManyField(Genre, related_name="users", blank=True)

    def __str__(self):
        return self.username
