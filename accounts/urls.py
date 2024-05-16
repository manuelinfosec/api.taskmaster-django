"""Account URLs"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from accounts.views import LoginAPI, ProfileAPI, RegisterAPI, UserUpdatePasswordAPI

urlpatterns = [
    path("auth/register/", RegisterAPI.as_view(), name="register_user"),
    path("auth/login/", LoginAPI.as_view(), name="login_user"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="user_token_verify"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="user_token_refresh"),
    path("auth/profile/", ProfileAPI.as_view(), name="get_update_profile"),
    path(
        "auth/profile/password/",
        UserUpdatePasswordAPI.as_view(),
        name="update_password",
    ),
]
