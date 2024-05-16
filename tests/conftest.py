import pytest
from django.contrib.auth import get_user_model
from faker import Faker
from pytest_factoryboy import register
from rest_framework.test import APIClient

from tests.factories import UserFactory

fake = Faker()


# register factories
register(UserFactory)


import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from faker import Faker

fake = Faker()


@pytest.fixture
def api_client():
    """
    Fixture for providing an instance of the Django REST Framework API client.

    Returns:
        APIClient: Instance of the Django REST Framework API client.
    """
    return APIClient


@pytest.fixture
def user_model():
    """
    Fixture for providing the User model class.

    Returns:
        Model: The User model class.
    """
    return get_user_model()


@pytest.fixture
def created_user(db, user_factory):
    """
    Fixture for creating a user instance with a password.

    Args:
        db: Django database fixture.
        user_factory: Factory for creating user instances.

    Returns:
        tuple: A tuple containing the created user instance and the password used.
    """
    password = fake.password(length=8)

    user = user_factory.create(password=password)

    return user, password
