"""Custom authentication backends"""

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db import models


class AuthUserBackend(ModelBackend):
    """
    Custom authentication backend for username/email and password authentication.

    This backend allows users to authenticate using either their username or email address,
    providing flexibility in the login process. It performs a case-insensitive search for
    the username/email field, ensuring that users can log in regardless of the case used
    in their input.

    Reasons for usage:
    1. Enhanced User Experience: Users can log in using either their username or email.
    2. Flexibility: Provides flexibility in the authentication process by supporting
       multiple login methods.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate the user based on username/email and password.

        Args:
            request: The HTTP request being authenticated.
            username: The username or email address provided for authentication.
            password: The password provided for authentication.
            **kwargs: Additional keyword arguments (not used).

        Returns:
            The authenticated user if successful, None otherwise.
        """
        try:
            # Perform a case-insensitive search for the username/email
            user = get_user_model()._default_manager.get(
                models.Q(username__exact=username) | models.Q(email__iexact=username)
            )
        except get_user_model().DoesNotExist:
            # User does not exist
            return None
        else:
            # Check if the password is valid and user can authenticate
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
            return None
