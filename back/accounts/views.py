from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer, RegisterSerializer
import logging

logger = logging.getLogger(__name__)  # 디버깅 로그 추가

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
        logger.info(f"프로필 조회: {user.username}")  # 프로필 조회 로그 추가
        return Response(serializer.data)
