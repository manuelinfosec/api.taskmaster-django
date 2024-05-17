"""Accounts serializers"""

import re

from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from rest_framework import exceptions, serializers, status

from taskmaster.utils import get_object_or_error


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user model.

    This serializer provides functionality to serialize and deserialize user data,
    including password hashing, validation, and lowercase transformation of username and email.

    Attributes:
        password: A CharField to handle password input.
    """

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
        """
        Lowercase username and email values.

        Args:
            data (dict): The input data.

        Returns:
            dict: The transformed input data with username and email in lowercase.
        """
        if data.get("username"):
            # Convert `username` to lowercase
            data["username"] = data["username"].lower()

        if data.get("email"):
            # Convert `email` to lowercase
            data["email"] = data["email"].lower()

        return super().to_internal_value(data)

    def create(self, validated_data):
        """
        Create a new user instance.

        Args:
            validated_data (dict): The validated data for user creation.

        Returns:
            User: The newly created user instance.
        """
        password = validated_data.pop(
            "password"
        )  # Extract the password from validated data

        # Create a new user instance using the extracted data
        user = get_user_model().objects.create(**validated_data)

        # Hash and set password for the user
        user.set_password(password)

        # Save the user object with the hashed password
        user.save()

        return user


class UserUpdatePasswordSerializer(serializers.Serializer):
    """
    Serializer for updating user password.

    This serializer validates and processes requests to update a user's password.

    Attributes:
        user_id (serializers.UUIDField): The unique identifier of the user.
        old_password (serializers.CharField): The old password of the user.
        new_password_1 (serializers.CharField): The new password entered by the user (first entry).
        new_password_2 (serializers.CharField): The new password entered by the user (second entry).

    Methods:
        validate: Validates the new passwords to ensure they match.
        save: Saves the new password for the user after validation.
    """

    user_id = serializers.UUIDField(required=True)  # Field for user ID
    old_password = serializers.CharField(
        required=True, min_length=6
    )  # Field for old password
    new_password_1 = serializers.CharField(
        required=True, min_length=6
    )  # Field for new password (first entry)
    new_password_2 = serializers.CharField(
        required=True, min_length=6
    )  # Field for new password (second entry)

    def validate(self, data):
        """
        Validate method to ensure new passwords match.

        Args:
            data (dict): Dictionary containing user input data.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If the new passwords do not match.
        """
        if data["new_password_2"] != data["new_password_1"]:
            raise serializers.ValidationError(
                detail={"new_password_2": "Value should be same as new_password_1"}
            )
        return data

    def save(self, **kwargs):
        """
        Save method to update user password.

        This method saves the new password for the user after validation.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: A dictionary confirming the password update.

        Raises:
            serializers.ValidationError: If the old password provided is incorrect.
        """

        # Retrieve the user object based on the provided user_id
        user = get_object_or_error(get_user_model(), id=self.validated_data["user_id"])

        # Check if the old password provided matches the user's current password
        if not user.check_password(self.validated_data["old_password"]):
            # Raise a validation error if the old password is incorrect
            raise serializers.ValidationError(
                detail={"old_password": "value provided is not correct"},
                code=status.HTTP_400_BAD_REQUEST,
            )

        # Hash and set the new password for the user
        user.set_password(self.validated_data["new_password_2"])

        # Save the updated user object with the new password
        user.save()

        # Return a success message indicating that the password has been updated successfully
        return {"detail": "password updated successfully"}


class LoginSerializer(serializers.Serializer):
    """
    Serializer class for user login authentication.

    This serializer handles the validation and authentication of user login credentials.
    It expects a username and password as input for authentication.

    Attributes:
        username: A CharField for the username.
        password: A CharField for the password, with write-only access.

    Methods:
        to_internal_value: Converts provided username and email values to lowercase.
        create: Authenticates the user based on provided credentials and updates
                the last login timestamp for the authenticated user.

    Raises:
        NotAuthenticated: If user authentication fails due to invalid credentials.
    """

    # Define fields for username and password
    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True, min_length=6, style={"input_type": "password"}
    )

    def to_internal_value(self, data):
        """Convert provided username and email values to lowercase."""
        if data.get("username"):
            # Convert username to lowercase if provided
            data["username"] = data["username"].lower()

        if data.get("email"):
            # Convert email to lowercase if provided
            data["email"] = data["email"].lower()

        return super().to_internal_value(data)

    def create(self, validated_data):
        """
        Authenticate the user based on provided credentials.

        Args:
            validated_data: A dictionary containing validated username and password.

        Returns:
            Authenticated user if successful.

        Raises:
            NotAuthenticated: If user authentication fails due to invalid credentials.
        """

        # Authenticate the user based on provided credentials
        user = authenticate(**validated_data)

        if not user:
            # Raise a NotAuthenticated exception if user authentication fails
            raise exceptions.NotAuthenticated(
                detail="Invalid login credentials", code=status.HTTP_401_UNAUTHORIZED
            )

        # Update the last login timestamp for the authenticated user
        user.last_login = timezone.now()
        user.save()

        # Return the authenticated user
        return user
