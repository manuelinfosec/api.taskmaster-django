"""Test authentication endpoints"""

import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

# Mark the entire test class to use Django DB and transactions
pytestmark = pytest.mark.django_db(transaction=True)
User = get_user_model()


class TestAuthEndpoints:
    """
    Test class for authentication endpoints.

    This class contains test cases for the authentication endpoints, including user registration, login,
    retrieval of user profile, updating user profile, and updating user password.
    """

    def test_register_user(self, api_client, user_factory):
        """Test registration of a new user."""

        # Create user data using the user factory
        user = user_factory.build()
        user_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "username": user.username,
            "password": user.password,
        }

        # Send a POST request to register a new user
        response = api_client.post(
            path=reverse("register_user"), data=user_data, format="json"
        )

        # Check if the response status code is HTTP 201 CREATED
        assert response.status_code == status.HTTP_201_CREATED

        # Check if the registered username matches the provided username
        assert user_data["username"] == response.data["username"]

    def test_login_user(self, api_client, created_user):
        """Test user login."""

        user, password = created_user

        # Send a POST request to login with user credentials
        response = api_client.post(
            path=reverse("login_user"),
            data=dict(username=user.username, password=password),
            format="json",
        )

        # Check if the response status code is HTTP 200 OK
        assert response.status_code == status.HTTP_200_OK

        # Check if the response contains user data
        assert "tokens" in response.data

    def test_get_user_profile(self, api_client, created_user):
        """Test retrieval of user profile."""

        user, _ = created_user

        # Send a GET request to retrieve user profile
        api_client.force_authenticate(user=user)
        response = api_client.get(reverse("get_update_profile"))

        # Check if the response status code is HTTP 200 OK
        assert response.status_code == status.HTTP_200_OK

        # Check if the response contains user data
        assert "email" in response.data
        assert "username" in response.data

    def test_update_user_profile(self, api_client, created_user):
        """Test updating of user profile."""

        user, _ = created_user

        # Send a GET request to retrieve user profile
        api_client.force_authenticate(user=user)
        # Send a PUT request to update user profile
        response = api_client.patch(
            reverse("get_update_profile"),
            data={"first_name": "New First Name", "last_name": "New Last Name"},
            format="json",
        )

        # Check if the response status code is HTTP 202 ACCEPTED
        assert response.status_code == status.HTTP_202_ACCEPTED

        # Check if the updated profile data matches the provided data
        assert response.data["first_name"] == "New First Name"
        assert response.data["last_name"] == "New Last Name"

    def test_update_user_password(self, api_client, created_user):
        """Test updating user's password."""

        user, password = created_user

        # Send a GET request to retrieve user profile
        api_client.force_authenticate(user=user)

        # Send a POST request to update user password
        response = api_client.post(
            reverse("update_password"),
            data={
                "old_password": password,
                "new_password_1": "new_password",
                "new_password_2": "new_password",
            },
            format="json",
        )

        # Check if the response status code is HTTP 200 OK
        assert response.status_code == status.HTTP_200_OK
