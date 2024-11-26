from django.urls import path
from .views import RegisterView, LoginView, ProfileView, check_field, CurrentUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path("check-<str:field>/", check_field, name="check-field"),
    path('me/', CurrentUserView.as_view(), name='current_user'),  # 현재 사용자 정보 엔드포인트 추가
]
