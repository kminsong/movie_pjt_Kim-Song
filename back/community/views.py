from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Count, Q
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination

class CommunityPagination(PageNumberPagination):
    page_size = 10  # 한 페이지에 보여줄 게시글 수
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostListCreateView(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CommunityPagination  # 페이지네이션 추가

    def get_queryset(self):
        queryset = Post.objects.all()
        filter_type = self.request.query_params.get("filter", "latest")
        is_hot = self.request.query_params.get("is_hot", "false").lower() == "true"
        search_query = self.request.query_params.get("search", "").strip()  # 검색어
        search_field = self.request.query_params.get("search_field", "title")  # 검색 필드

        if is_hot:
            queryset = queryset.filter(is_hot=True)

        if filter_type == "likes":
            queryset = queryset.order_by("-likes", "-created_at")
        elif filter_type == "comments":
            queryset = queryset.annotate(comment_count=Count("comments")).order_by(
                "-comment_count", "-created_at"
            )
        else:
            queryset = queryset.order_by("-created_at")

        # 검색 필드별로 필터링
        if search_query:
            if search_field == "title":
                queryset = queryset.filter(title__icontains=search_query)
            elif search_field == "author":
                queryset = queryset.filter(author__nickname__icontains=search_query)
            elif search_field == "content":
                queryset = queryset.filter(content__icontains=search_query)

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # 좋아요/싫어요 상태 추가
        user = request.user
        data["liked_by_user"] = user in instance.liked_users.all() if user.is_authenticated else False
        data["disliked_by_user"] = user in instance.disliked_users.all() if user.is_authenticated else False

        return Response(data)


class CommentListCreateView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs["post_id"])
        serializer.save(author=self.request.user, post=post)

class CommentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return Comment.objects.filter(post_id=post_id)

class PostLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        try:
            post = Post.objects.get(pk=pk)

            # 본인 작성 글인지 확인
            if post.author == request.user:
                return Response(
                    {"error": "본인의 글에는 좋아요를 누를 수 없습니다."},
                    status=403,
                )

            # 중복 좋아요 방지
            if request.user in post.liked_users.all():
                post.liked_users.remove(request.user)
                post.likes -= 1
                post.save()
                return Response(
                    {"likes": post.likes, "message": "좋아요 취소됨"}, status=200
                )

            # 좋아요 추가
            post.liked_users.add(request.user)
            post.likes += 1
            post.save()
            return Response(
                {"likes": post.likes, "message": "좋아요 추가됨"}, status=200
            )

        except Post.DoesNotExist:
            return Response(
                {"error": "게시글을 찾을 수 없습니다."}, status=404
            )


class PostDislikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        try:
            post = Post.objects.get(pk=pk)

            # 본인 작성 글인지 확인
            if post.author == request.user:
                return Response(
                    {"error": "본인의 글에는 싫어요를 누를 수 없습니다."},
                    status=403,
                )

            # 중복 싫어요 방지
            if request.user in post.disliked_users.all():
                post.disliked_users.remove(request.user)
                post.dislikes -= 1
                post.save()
                return Response(
                    {"dislikes": post.dislikes, "message": "싫어요 취소됨"}, status=200
                )

            # 싫어요 추가
            post.disliked_users.add(request.user)
            post.dislikes += 1
            post.save()
            return Response(
                {"dislikes": post.dislikes, "message": "싫어요 추가됨"}, status=200
            )

        except Post.DoesNotExist:
            return Response(
                {"error": "게시글을 찾을 수 없습니다."}, status=404
            )
