from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post", "author_name", "content", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.nickname", read_only=True)
    comment_count = serializers.IntegerField(source="comments.count", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author_name",
            "created_at",
            "updated_at",
            "likes",
            "dislikes",
            "is_hot",
            "comment_count",
        ]
