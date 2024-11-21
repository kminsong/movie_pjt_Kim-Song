from django.db import models
from django.conf import settings  # settings.AUTH_USER_MODEL 가져오기

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # 카테고리 이름

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)  # 제목
    content = models.TextField()  # 내용
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 작성자
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # 카테고리
    created_at = models.DateTimeField(auto_now_add=True)  # 작성일
    updated_at = models.DateTimeField(auto_now=True)  # 수정일
    likes = models.PositiveIntegerField(default=0)  # 좋아요 수
    dislikes = models.PositiveIntegerField(default=0)  # 싫어요 수
    is_hot = models.BooleanField(default=False)  # Hot 글 여부

    def save(self, *args, **kwargs):
        # 좋아요/싫어요 비율로 Hot 글 판단
        if self.likes >= 20 and (self.likes / max(1, self.dislikes)) >= 3:
            self.is_hot = True
        else:
            self.is_hot = False
        super().save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")  # 게시글
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 작성자
    content = models.TextField()  # 댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 작성일
