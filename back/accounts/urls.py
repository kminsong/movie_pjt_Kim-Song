from django.urls import path
from .views import RegisterView, LoginView, ProfileView, NicknameCheckView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),  # GET, PUT, DELETE 지원
    path('check-nickname/', NicknameCheckView.as_view(), name='check_nickname'),
]
