from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/movies/', include('movies.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/community/', include('community.urls')),  # community 경로 연결
]
