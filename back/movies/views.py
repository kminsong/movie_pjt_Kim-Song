from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Genre
from .serializers import MovieSerializer
from django.db.models import Q

class MoviePagination(PageNumberPagination):
    """Pagination 설정"""
    page_size = 10  # 기본 한 페이지당 항목 수
    page_size_query_param = 'page_size'  # 클라이언트에서 요청할 경우 페이지 크기 설정
    max_page_size = 100  # 최대 페이지 크기 제한

class MovieList(ListAPIView):
    """영화 목록 조회"""
    serializer_class = MovieSerializer
    pagination_class = MoviePagination

    def get_queryset(self):
        # 필터 조건 받기
        genres = self.request.query_params.getlist('genres')  # 장르 필터
        order_by = self.request.query_params.get('order_by', 'release_date')  # 정렬 옵션
        queryset = Movie.objects.filter(adult=False)  # 기본적으로 성인 콘텐츠 제외

        # 장르 필터링 (교집합)
        if genres:
            queryset = queryset.filter(genres__name__in=genres).distinct()
            for genre in genres:
                queryset = queryset.filter(genres__name=genre)

        # 정렬 적용
        if order_by == 'popularity':
            queryset = queryset.order_by('-popularity')
        elif order_by == 'release_date':
            queryset = queryset.order_by('-release_date')

        return queryset

        queryset = Movie.objects.filter(adult=False)  # 기본적으로 성인 콘텐츠 제외

        # 장르 필터링 (교집합)
        if genres:
            queryset = queryset.filter(genres__name__in=genres).distinct()
            for genre in genres:
                queryset = queryset.filter(genres__name=genre)

        # 정렬 적용
        if order_by == 'popularity':
            queryset = queryset.order_by('-popularity')
        elif order_by == 'release_date':
            queryset = queryset.order_by('-release_date')

        return queryset
