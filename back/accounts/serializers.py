from rest_framework import serializers
from .models import User
from movies.models import Genre

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'nickname', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        """
        이메일 중복 검사를 수행하지만 공백은 중복 검사를 하지 않음.
        """
        if value:  # 이메일 값이 제공된 경우에만 중복 체크
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("이미 사용 중인 이메일입니다.")
        return value  # 이메일이 None일 경우 빈 문자열 반환

    def create(self, validated_data):
        # 비밀번호 분리
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # 비밀번호 암호화
        user.save()
        return user

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
