import uuid

from django.contrib.auth import get_user_model
from django.utils import timezone

from accounts.serializers import UserSerializer, LoginSerializer, UserUpdatePasswordSerializer

from taskmaster.utils import (
    generate_user_tokens,
    get_object_or_error,
    remove_none_values,
    paginate_queryset
)

User = get_user_model()


class AuthService:
    @staticmethod
    def register_user(
        first_name=None,
        last_name=None,
        username=None,
        email=None,
        password=None,
    ):

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
        serializer = LoginSerializer(data={"username": username, "password": password})

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return {
            **UserSerializer(serializer.instance).data,
            "tokens": generate_user_tokens(serializer.instance),
        }

    @staticmethod
    def get_user(user_id, auth_provider=None, auth_provider_id=None):
        user = get_object_or_error(
            User,
            id=user_id,
            **remove_none_values(
                {
                    "auth_provider": auth_provider,
                    "auth_provider_id": auth_provider_id,
                }
            )
        )

        return UserSerializer(user).data

    @staticmethod
    def list_users(request, page: int = 1):
        users = User.objects.all()

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
        phone_number=None,
        user_type=None,
        is_staff=None,
    ):
        user = get_object_or_error(User, id=user_id)
        user_update_serializer = UserSerializer(
            user,
            data=remove_none_values(
                {
                    "first_name": first_name,
                    "last_name": last_name,
                    "username": username,
                    "email": email,
                    "phone_number": phone_number,
                    "user_type": user_type,
                    "is_staff": is_staff,
                }
            ),
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
        user = get_object_or_error(User, id=user_id)
        user.delete()
