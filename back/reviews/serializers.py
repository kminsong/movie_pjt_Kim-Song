from rest_framework import serializers
from .models import Review
from movies.models import Movie

class ReviewSerializer(serializers.ModelSerializer):
    movie_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        fields = ['id', 'movie_id', 'title', 'content', 'like_count', 'created_at', 'updated_at']
        read_only_fields = ['like_count', 'created_at', 'updated_at']

    def validate_movie_id(self, value):
        print(f"validate_movie_id - 입력된 movie_id: {value}")
        try:
            movie = Movie.objects.get(tmdb_id=value)
            return movie
        except Movie.DoesNotExist:
            raise serializers.ValidationError("유효하지 않은 TMDB ID입니다.")

    def create(self, validated_data):
        movie = validated_data.pop('movie_id')
        review = Review.objects.create(movie=movie, **validated_data)
        return review
