from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from rest_framework.permissions import AllowAny

from users.apps import UsersConfig

from users.views import UserCreateAPIView, UserProfileRetrieveAPIView, UserUpdateAPIView, UserListAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', UserCreateAPIView.as_view(), name='login'),
    path('users/<int:pk>/', UserProfileRetrieveAPIView.as_view(), name='users_retrieve'),
    path('users/<int:pk>/update/', UserUpdateAPIView.as_view(), name='users_update'),
    path("", UserListAPIView.as_view(), name="user_list"),

    path('token/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
]

