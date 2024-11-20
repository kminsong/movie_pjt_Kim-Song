from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Review
from movies.models import Movie
from .serializers import ReviewSerializer
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError


class ReviewPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ReviewListCreate(ListCreateAPIView):
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Review.objects.all().order_by('-created_at')
        movie_id = self.request.query_params.get('movie_id', None)
        search = self.request.query_params.get('search', None)
        filter_by = self.request.query_params.get('filter', 'title')

        # 영화 ID로 필터링
        if movie_id:
            queryset = queryset.filter(movie__tmdb_id=movie_id)

        # 제목 또는 영화 제목으로 검색
        if search:
            if filter_by == 'movie_title':
                queryset = queryset.filter(movie__title__icontains=search)
            else:
                queryset = queryset.filter(title__icontains=search)

        # 좋아요 순 정렬
        if self.request.query_params.get('order_by') == 'likes':
            queryset = queryset.order_by('-like_count')

        return queryset

    def perform_create(self, serializer):
        movie_id = self.request.data.get("movie_id")
        print(f"Received movie_id: {movie_id}")  # 디버깅 로그
        if not movie_id:
            raise ValidationError({"movie_id": "movie_id 필드가 누락되었습니다."})

        try:
            movie = Movie.objects.get(tmdb_id=movie_id)
        except Movie.DoesNotExist:
            
            raise ValidationError({"movie_id": "유효하지 않은 movie_id 입니다."})

        serializer.save(user=self.request.user)


class TopReviewsForMovie(APIView):
    def get(self, request, movie_id):
        reviews = Review.objects.filter(movie__tmdb_id=movie_id).order_by('-like_count')[:3]
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class ReviewDetailAPIView(RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
