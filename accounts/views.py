"""Account APIs"""

from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from accounts.services import AuthService
from taskmaster.permissions import IsAuthenticated, IsObjectOwner
from taskmaster.utils import get_object_or_error

auth_service = AuthService()


class RegisterAPI(generics.GenericAPIView):
    """
    Endpoint for user registration.

    URL: /auth/register/
    """

    # Set permission_classes to AllowAny to ignore authorization headers
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Accepts POST requests with user registration data including first name, last name,
        username, email, and password.

        Returns:
            - HTTP 201 Created: If user registration is successful.
        """
        return Response(
            data=auth_service.register_user(
                first_name=request.data.get("first_name"),
                last_name=request.data.get("last_name"),
                username=request.data.get("username"),
                email=request.data.get("email"),
                password=request.data.get("password"),
            ),
            status=status.HTTP_201_CREATED,
        )


class LoginAPI(generics.GenericAPIView):
    """
    Endpoint for user login.

    URL: /auth/login/
    """

    # Set permission_classes to AllowAny to ignore authorization headers
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Accepts POST requests with user credentials (username and password).

        Returns:
            - HTTP 200 OK: If user authentication is successful.
        """
        return Response(
            data=auth_service.login_user(
                username=request.data.get("username") or request.data.get("email"),
                password=request.data.get("password"),
            ),
            status=status.HTTP_200_OK,
        )


class ProfileAPI(generics.GenericAPIView):
    """
    Endpoint for accessing and updating user profile.

    URL: /auth/profile/

    Requires authentication and only allows access to the profile of the authenticated user.
    """

    permission_classes = [IsAuthenticated, IsObjectOwner]

    def get_object(self):
        obj = get_object_or_error(get_user_model(), id=self.request.user.id)
        self.check_object_permissions(self.request, obj.id)

        obj = auth_service.get_user(user_id=obj.id)
        return obj

    def get(self, request):
        """
        Accepts GET requests to retrieve user profile data

        Returns:
        - HTTP 200 OK: If GET request for user profile data is successful.
        """
        return Response(
            data=auth_service.get_user(
                user_id=request.user.id,
            ),
            status=status.HTTP_200_OK,
        )

    def patch(self, request):
        """
        PUT requests to update user profile data.

        Returns:
        - HTTP 202 Accepted: If PUT request to update user profile data is successful.
        """
        self.get_object()

        return Response(
            data=auth_service.update_user(
                user_id=request.user.id,
                first_name=request.data.get("first_name"),
                last_name=request.data.get("last_name"),
                username=request.data.get("username"),
                email=request.data.get("email"),
            ),
            status=status.HTTP_202_ACCEPTED,
        )


class UserUpdatePasswordAPI(generics.GenericAPIView):
    """
    Endpoint for updating user password.

    URL: /auth/profile/password/

    Requires authentication.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Accepts POST requests with old password, new password, and password confirmation.

        Returns:
        - HTTP 200 OK: If password update is successful.
        """
        return Response(
            data=auth_service.update_user_password(
                user_id=request.user.id,
                old_password=request.data.get("old_password"),
                new_password_1=request.data.get("new_password_1"),
                new_password_2=request.data.get("new_password_2"),
            ),
            status=status.HTTP_200_OK,
        )
