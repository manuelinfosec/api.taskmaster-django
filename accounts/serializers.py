import re

from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from rest_framework import exceptions, serializers, status

from taskmaster.utils import get_object_or_error


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True, min_length=6, required=False, style={"input_type": "password"}
    )

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "last_updated",
            "last_login",
            "password",
            "is_superuser",
        )

    def to_internal_value(self, data):
        """lowercase  username and email values."""
        if data.get("username"):
            data["username"] = data["username"].lower()

        if data.get("email"):
            data["email"] = data["email"].lower()

        return super().to_internal_value(data)

    def validate_phone_number(self, value):
        phone_number_format = re.compile("[+]?\d{11,14}$")

        if value:
            if not phone_number_format.match(value):
                raise serializers.ValidationError(
                    detail="Phone number is incorrect", code=status.HTTP_400_BAD_REQUEST
                )

        return value

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = get_user_model().objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user


class UserUpdatePasswordSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(required=True)
    old_password = serializers.CharField(required=True, min_length=6, max_length=16)
    new_password_1 = serializers.CharField(required=True, min_length=6, max_length=16)
    new_password_2 = serializers.CharField(required=True, min_length=6, max_length=16)

    def validate(self, data):
        if data["new_password_2"] != data["new_password_1"]:
            raise serializers.ValidationError(
                detail={"new_password_2": "Value should be same as new_password_1"}
            )
        return data

    def save(self, **kwargs):
        user = get_object_or_error(get_user_model(), id=self.validated_data["user_id"])

        if not user.check_password(self.validated_data["old_password"]):
            raise serializers.ValidationError(
                detail={"old_password": "value provided is not correct"},
                code=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(self.validated_data["new_password_2"])
        user.save()

        return {"detail": "password updated successfully"}


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True, min_length=6, style={"input_type": "password"}
    )

    def to_internal_value(self, data):
        """lowercase  username and email values."""
        if data.get("username"):
            data["username"] = data["username"].lower()

        if data.get("email"):
            data["email"] = data["email"].lower()

        return super().to_internal_value(data)

    def create(self, validated_data):
        user = authenticate(**validated_data)

        if not user:
            raise exceptions.NotAuthenticated(
                detail="Invalid login credentials", code=status.HTTP_401_UNAUTHORIZED
            )

        user.last_login = timezone.now()
        user.save()

        return user
