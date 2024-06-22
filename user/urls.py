from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='user_login'),
    path('refresh_token/', TokenRefreshView.as_view(), name='user_refresh_token'),
]
