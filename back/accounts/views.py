from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from .models import User
from movies.models import Genre
from .serializers import UserSerializer, RegisterSerializer
import logging

logger = logging.getLogger(__name__)  # 디버깅 로그 추가
User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.info(f"요청 데이터: {request.data}")  # 요청 데이터 로그 추가
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            logger.info(f"회원가입 성공! 사용자: {user.username}")  # 성공 로그 추가
            return Response({
                "message": "회원가입 성공!",
                "token": token.key,
                "user": UserSerializer(user).data,
            }, status=HTTP_200_OK)
        logger.error(f"유효성 검사 실패: {serializer.errors}")  # 유효성 검사 실패 로그 추가
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        logger.info(f"로그인 시도: {username}")  # 디버깅 로그 추가
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            logger.info(f"로그인 성공: {username}")  # 성공 로그 추가
            return Response({
                "message": "로그인 성공!",
                "token": token.key,
                "user": UserSerializer(user).data,
            }, status=HTTP_200_OK)
        logger.error("로그인 실패: 아이디 또는 비밀번호가 잘못되었습니다.")  # 실패 로그 추가
        return Response({"error": "아이디 또는 비밀번호가 잘못되었습니다."}, status=HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        data = request.data.copy()

        # 'favorite_genres' 필드 처리
        favorite_genres_ids = data.pop('favorite_genres', None)
        if favorite_genres_ids is not None:
            try:
                genres = Genre.objects.filter(id__in=favorite_genres_ids)
                if len(genres) != len(favorite_genres_ids):
                    invalid_ids = set(favorite_genres_ids) - set(genres.values_list('id', flat=True))
                    return Response(
                        {"error": f"Invalid genre IDs provided: {list(invalid_ids)}"},
                        status=400
                    )
                user.favorite_genres.set(genres)
            except Exception as e:
                return Response({"error": str(e)}, status=400)

        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request):
        user = request.user
        logger.info(f"회원 탈퇴 시도: {user.username}")
        user.delete()
        return Response({"message": "회원 탈퇴가 완료되었습니다."}, status=HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([AllowAny])
def check_field(request, field):
    """
    특정 필드(username, email, nickname) 중복 검사
    """
    if field not in ["username", "email", "nickname"]:
        return Response({"error": "허용되지 않은 필드입니다."}, status=400)

    value = request.query_params.get(field)
    if not value:
        return Response({"error": f"{field} 값이 필요합니다."}, status=400)

    is_available = not User.objects.filter(**{field: value}).exists()
    return Response({"is_available": is_available})

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        현재 로그인한 사용자의 정보를 반환합니다.
        """
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
