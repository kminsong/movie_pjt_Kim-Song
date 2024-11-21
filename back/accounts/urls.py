from django.urls import path
from .views import RegisterView, LoginView, ProfileView, NicknameCheckView, CurrentUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('check-nickname/', NicknameCheckView.as_view(), name='check_nickname'),
    # ------------------------- [수정된 부분 시작] -------------------------
    path('me/', CurrentUserView.as_view(), name='current_user'),  # 현재 사용자 정보 엔드포인트 추가
    # ------------------------- [수정된 부분 끝] -------------------------
]
