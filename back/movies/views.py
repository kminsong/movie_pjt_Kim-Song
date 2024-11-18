from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Movie
from .serializers import MovieSerializer

class MoviePagination(PageNumberPagination):
    """Pagination 설정"""
    page_size = 10  # 기본 한 페이지당 항목 수
    page_size_query_param = 'page_size'  # 클라이언트에서 요청할 경우 페이지 크기 설정
    max_page_size = 100  # 최대 페이지 크기 제한


class MovieList(ListAPIView):
    """영화 목록 조회"""
    queryset = Movie.objects.filter(adult=False)  # 성인 콘텐츠 제외
    serializer_class = MovieSerializer
    pagination_class = MoviePagination


class MovieCreate(CreateAPIView):
    """영화 추가"""
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
