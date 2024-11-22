from django.urls import path
from .views import (
    PostListCreateView,
    PostDetailView,
    CommentListCreateView,
    PostLikeAPIView,
    PostDislikeAPIView,
)

urlpatterns = [
    path("posts/", PostListCreateView.as_view(), name="post-list-create"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/<int:pk>/like/", PostLikeAPIView.as_view(), name="post-like"),
    path("posts/<int:pk>/dislike/", PostDislikeAPIView.as_view(), name="post-dislike"),
    path("posts/<int:post_id>/comments/", CommentListCreateView.as_view(), name="comment-list-create"),
]
