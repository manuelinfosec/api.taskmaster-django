import uuid

from django.contrib.auth import get_user_model
from django.utils import timezone

from accounts.serializers import (
    LoginSerializer,
    UserSerializer,
    UserUpdatePasswordSerializer,
)
from taskmaster.utils import (
    generate_user_tokens,
    get_object_or_error,
    paginate_queryset,
    remove_none_values,
)

User = get_user_model()


class AuthService:
    """
    Service class for user authentication and management.

    This class provides static methods for registering, logging in, retrieving, updating,
    and deleting user accounts. It interacts with serializers and utility functions to perform
    these actions.

    Methods:
        register_user: Registers a new user with the provided data.
        login_user: Logs in a user with the provided username and password.
        get_user: Retrieves user data based on the user ID or authentication provider details.
        list_users: Retrieves a paginated list of all users.
        update_user: Updates user information based on the provided data.
        update_user_password: Updates the password for a user account.
        delete_user: Deletes a user account based on the user ID.

    """

    @staticmethod
    def register_user(
        first_name=None,
        last_name=None,
        username=None,
        email=None,
        password=None,
    ):
        """
        Registers a new user with the provided data.

        Args:
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            username (str): The username of the user.
            email (str): The email address of the user.
            password (str): The password for the user.

        Returns:
            dict: User data along with generated authentication tokens.

        """
        serializer = None

        user_data = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "email": email,
            "last_login": timezone.now(),
        }

        serializer = UserSerializer(data={"password": password, **user_data})

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return {**serializer.data, "tokens": generate_user_tokens(serializer.instance)}

    @staticmethod
    def login_user(username, password):
        """
        Logs in a user with the provided username and password.

        Args:
            username (str): The username of the user.
            password (str): The password for the user.

        Returns:
            dict: User data along with generated authentication tokens.

        """
        serializer = LoginSerializer(data={"username_or_email": username, "password": password})

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return {
            **UserSerializer(serializer.instance).data,
            "tokens": generate_user_tokens(serializer.instance),
        }

    @staticmethod
    def get_user(user_id):
        """
        Retrieves user data based on the user ID or authentication provider details.

        Args:
            user_id (uuid.UUID): The ID of the user.
            auth_provider (str, optional): The authentication provider name.
            auth_provider_id (str, optional): The ID provided by the authentication provider.

        Returns:
            dict: Serialized user data.

        """
        user = get_object_or_error(
            User,
            id=user_id,
        )

        return UserSerializer(user).data

    @staticmethod
    def list_users(request, page: int = 1):
        """
        Retrieves a paginated list of all users.

        Args:
            request: The HTTP request object.
            page (int, optional): The page number for pagination.

        Returns:
            dict: Serialized user data.

        """
        users = User.objects.all()

        # Retrieve paginated data for the list of users
        paginated_data = paginate_queryset(
            queryset=users,
            serializer_class=UserSerializer,
            page=page,
            request=request,
        )
        serialized_data = paginated_data.data
        return serialized_data

    @staticmethod
    def update_user(
        user_id,
        first_name=None,
        last_name=None,
        username=None,
        email=None,
    ):
        """
        Updates user information based on the provided data.

        Args:
            user_id (uuid.UUID): The ID of the user.
            first_name (str, optional): The updated first name of the user.
            last_name (str, optional): The updated last name of the user.
            username (str, optional): The updated username of the user.
            email (str, optional): The updated email address of the user.

        Returns:
            dict: Serialized updated user data.

        """
        user = get_object_or_error(User, id=user_id)
        user_update_serializer = UserSerializer(
            user,
            # Remove `null` values
            data=remove_none_values(
                {
                    "first_name": first_name,
                    "last_name": last_name,
                    "username": username,
                    "email": email,
                }
            ),
            # Allow partial update for specified fields
            partial=True,
        )
        user_update_serializer.is_valid(raise_exception=True)
        user_update_serializer.save()

        return user_update_serializer.data

    @staticmethod
    def update_user_password(
        user_id: uuid.UUID,
        old_password: str,
        new_password_1: str,
        new_password_2: str,
    ):
        """
        Updates the password for a user account.

        Args:
            user_id (uuid.UUID): The ID of the user.
            old_password (str): The current password of the user.
            new_password_1 (str): The new password for the user.
            new_password_2 (str): The new password confirmation.

        Returns:
            dict: Serialized user data with updated password.

        """
        password_serializer = UserUpdatePasswordSerializer(
            data={
                "user_id": user_id,
                "old_password": old_password,
                "new_password_1": new_password_1,
                "new_password_2": new_password_2,
            }
        )

        password_serializer.is_valid(raise_exception=True)
        return password_serializer.save()

    @staticmethod
    def delete_user(user_id):
        """
        Deletes a user account based on the user ID.

        Args:
            user_id (uuid.UUID): The ID of the user to be deleted.

        """
        user = get_object_or_error(User, id=user_id)
        user.delete()
