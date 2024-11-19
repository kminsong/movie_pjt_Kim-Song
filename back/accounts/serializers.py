from rest_framework import serializers
from .models import User
from movies.models import Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class RegisterSerializer(serializers.ModelSerializer):
    favorite_genres = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'nickname', 'favorite_genres']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        favorite_genres = validated_data.pop('favorite_genres')
        user = User.objects.create_user(**validated_data)
        user.favorite_genres.set(favorite_genres)  # 필드 이름 수정
        return user

class UserSerializer(serializers.ModelSerializer):
    favorite_genres = GenreSerializer(many=True)  # 좋아하는 장르 직렬화

    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'email', 'favorite_genres']
