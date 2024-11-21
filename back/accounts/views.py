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


class NicknameCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        nickname = request.query_params.get('nickname')
        logger.info(f"닉네임 중복 검사 요청: {nickname}")  # 디버깅 로그 추가
        if not nickname:
            logger.error("닉네임이 제공되지 않았습니다.")  # 오류 로그 추가
            return Response({"error": "닉네임을 입력해주세요."}, status=HTTP_400_BAD_REQUEST)

        is_available = not User.objects.filter(nickname=nickname).exists()
        if is_available:
            logger.info(f"닉네임 사용 가능: {nickname}")  # 사용 가능 로그
        else:
            logger.info(f"닉네임 사용 불가: {nickname}")  # 사용 불가 로그
        return Response({"is_available": is_available}, status=HTTP_200_OK)


# ------------------------- [수정된 부분 시작] -------------------------
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        현재 로그인한 사용자의 정보를 반환합니다.
        """
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
# ------------------------- [수정된 부분 끝] -------------------------
