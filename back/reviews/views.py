from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Review, ReviewLike
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

        # 제목, 영화 제목, 작성자 검색
        if search:
            if filter_by == 'movie_title':
                queryset = queryset.filter(movie__title__icontains=search)
            elif filter_by == 'user_nickname':
                queryset = queryset.filter(user__nickname__icontains=search)
            else:
                queryset = queryset.filter(title__icontains=search)

        # 좋아요 순 정렬
        if self.request.query_params.get('order_by') == 'likes':
            queryset = queryset.order_by('-like_count')

        # 평점 순 정렬
        if self.request.query_params.get('order_by') == 'rating':
            queryset = queryset.order_by('-star_rating')

        return queryset

    def perform_create(self, serializer):
        movie_id = self.request.data.get("movie_id")
        if not movie_id:
            raise ValidationError({"movie_id": "movie_id 필드가 누락되었습니다."})

        try:
            movie = Movie.objects.get(tmdb_id=movie_id)
        except Movie.DoesNotExist:
            raise ValidationError({"movie_id": "유효하지 않은 movie_id 입니다."})

        # serializer의 validated_data에 movie 객체를 추가
        serializer.validated_data['movie'] = movie
        serializer.save(user=self.request.user)


class TopReviewsForMovie(APIView):
    def get(self, request, movie_id):
        reviews = Review.objects.filter(movie__tmdb_id=movie_id).order_by('-like_count')[:3]
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def update(self, request, *args, **kwargs):
        """
        PUT 요청 처리 (partial=True로 일부 필드만 업데이트 허용)
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)  # partial=True 추가

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


class LikeReview(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, review_id):
        try:
            review = Review.objects.get(pk=review_id)

            # 본인이 작성한 리뷰인지 확인
            if review.user == request.user:
                return Response({"error": "본인의 리뷰에는 좋아요를 누를 수 없습니다."}, status=403)

            # 중복 좋아요 방지
            like, created = ReviewLike.objects.get_or_create(user=request.user, review=review)

            if not created:
                # 이미 좋아요를 눌렀다면 삭제(좋아요 취소)
                like.delete()
                review.like_count -= 1
                review.save()
                return Response({"like_count": review.like_count, "message": "좋아요 취소됨"}, status=200)

            # 좋아요 추가
            review.like_count += 1
            review.save()
            return Response({"like_count": review.like_count, "message": "좋아요 추가됨"}, status=200)

        except Review.DoesNotExist:
            return Response({"error": "리뷰를 찾을 수 없습니다."}, status=404)
