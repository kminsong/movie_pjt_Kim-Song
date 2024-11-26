from rest_framework import serializers
from .models import Review
from movies.models import Movie

class ReviewSerializer(serializers.ModelSerializer):
    movie_id = serializers.IntegerField(write_only=True)  # 작성 시 사용할 movie_id
    movie_tmdb_id = serializers.IntegerField(source="movie.tmdb_id", read_only=True)  # 응답 데이터에 포함할 movie_id
    movie_title = serializers.CharField(source="movie.title", read_only=True)  # 영화 제목
    movie_poster = serializers.CharField(source="movie.poster_path", read_only=True)  # 영화 포스터 경로 추가
    user_nickname = serializers.CharField(source="user.nickname", read_only=True)  # 작성자 닉네임 추가
    user_id = serializers.IntegerField(source="user.id", read_only=True)  # 작성자 ID 추가
    liked_by_user = serializers.SerializerMethodField()  # 사용자가 좋아요를 눌렀는지 여부
    star_rating = serializers.FloatField()  # 별점 필드 추가 (최대 5, 반개 가능)

    class Meta:
        model = Review
        fields = [
            'id', 'movie_id', 'movie_tmdb_id', 'movie_title', 'movie_poster', 'title', 'content',
            'like_count', 'created_at', 'updated_at', 'user_nickname',
            'liked_by_user', 'user_id', 'star_rating',  # 별점 추가
        ]
        read_only_fields = [
            'movie_tmdb_id', 'movie_title', 'movie_poster', 'like_count', 'created_at', 'updated_at',
            'user_nickname', 'liked_by_user', 'user_id',
        ]

    def get_liked_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def validate_movie_id(self, value):
        """
        영화 ID가 유효한지 확인
        """
        try:
            movie = Movie.objects.get(tmdb_id=value)
            return movie  # Movie 객체 반환
        except Movie.DoesNotExist:
            raise serializers.ValidationError("유효하지 않은 TMDB ID입니다.")

    def validate_star_rating(self, value):
        """
        별점 유효성 검증 (0 ~ 5 사이)
        """
        if value < 0 or value > 5:
            raise serializers.ValidationError("별점은 0에서 5 사이의 값을 입력해야 합니다.")
        return value

    def create(self, validated_data):
        """
        새 리뷰 생성
        """
        movie = validated_data.pop('movie_id')  # validate_movie_id에서 반환된 Movie 객체
        validated_data['movie'] = movie  # validated_data에 Movie 객체 추가
        return super().create(validated_data)
