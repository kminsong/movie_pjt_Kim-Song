from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/movies/', include('movies.urls')),
    path('api/accounts/', include('accounts.urls')),  # accounts 경로 유지
    path('api/reviews/', include('reviews.urls')),  # 리뷰 관련 경로
]
