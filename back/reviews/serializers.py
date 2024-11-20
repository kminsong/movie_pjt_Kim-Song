from rest_framework import serializers
from .models import Review
from movies.models import Movie

class ReviewSerializer(serializers.ModelSerializer):
    movie_id = serializers.IntegerField(write_only=True)
    movie_title = serializers.CharField(source="movie.title", read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'movie_id', 'movie_title', 'title', 'content', 'like_count', 'created_at', 'updated_at']
        read_only_fields = ['movie_title', 'like_count', 'created_at', 'updated_at']

    def validate_movie_id(self, value):
        print(f"validate_movie_id - 입력된 movie_id: {value}")
        try:
            movie = Movie.objects.get(tmdb_id=value)
            return movie
        except Movie.DoesNotExist:
            raise serializers.ValidationError("유효하지 않은 TMDB ID입니다.")

    def create(self, validated_data):
        movie = validated_data.pop('movie_id')  # movie_id를 pop하여 Movie 객체로 변환
        validated_data['movie'] = movie
        return super().create(validated_data)
