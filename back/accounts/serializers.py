from rest_framework import serializers
from .models import User
from movies.models import Genre


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'nickname']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # 새로운 사용자 생성
        return User.objects.create_user(**validated_data)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    favorite_genres = GenreSerializer(many=True, read_only=True)  # 읽기 시 직렬화
    favorite_genres_ids = serializers.ListField(  # 쓰기 시 사용
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'email', 'favorite_genres', 'favorite_genres_ids']

    def update(self, instance, validated_data):
        favorite_genres_ids = validated_data.pop('favorite_genres_ids', None)
        if favorite_genres_ids:
            genres = Genre.objects.filter(id__in=favorite_genres_ids)
            instance.favorite_genres.set(genres)
        return super().update(instance, validated_data)
