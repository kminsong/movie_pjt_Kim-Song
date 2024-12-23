from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.nickname", read_only=True)
    author_id = serializers.IntegerField(source="author.id", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post", "author_name", "author_id", "content", "created_at"]

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.nickname", read_only=True)
    author_id = serializers.IntegerField(source="author.id", read_only=True)  # 작성자 ID 추가
    comment_count = serializers.IntegerField(source="comments.count", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author_name",
            "author_id",  # 작성자 ID 필드 추가
            "created_at",
            "updated_at",
            "likes",
            "dislikes",
            "is_hot",
            "comment_count",
        ]