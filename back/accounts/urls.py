from django.urls import path
from .views import RegisterView, LoginView, ProfileView, NicknameCheckView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('check-nickname/', NicknameCheckView.as_view(), name='check_nickname'),  # 닉네임 중복 검사 추가
]
