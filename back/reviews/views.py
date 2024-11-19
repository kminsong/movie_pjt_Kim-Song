from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Review
from movies.models import Movie
from .serializers import ReviewSerializer
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

class ReviewPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ReviewList(ListAPIView):
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination

    def get_queryset(self):
        queryset = Review.objects.all().order_by('-created_at')  # 기본 정렬: 최신순
        search = self.request.query_params.get('search', None)
        filter_by = self.request.query_params.get('filter', 'title')

        # 제목 또는 영화 제목으로 검색
        if search:
            if filter_by == 'movie_title':
                queryset = queryset.filter(movie__title__icontains=search)
            else:  # 기본 검색: 리뷰 제목
                queryset = queryset.filter(title__icontains=search)
        
        # 좋아요 순 정렬
        if self.request.query_params.get('order_by') == 'likes':
            queryset = queryset.order_by('-like_count')

        return queryset

class ReviewCreate(ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # 작성자 자동 저장

# 특정 영화의 상위 3개 리뷰 가져오기
class TopReviewsForMovie(APIView):
    def get(self, request, movie_id):
        reviews = Review.objects.filter(movie__id=movie_id).order_by('-like_count')[:3]
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
