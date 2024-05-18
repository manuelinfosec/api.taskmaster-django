import pytest
from django.db.utils import DataError, IntegrityError
from faker import Faker

pytestmark = pytest.mark.django_db(transaction=True)
fake = Faker()


class TestUserModel:
    """
    Test class for the User model.

    This class contains test cases for various aspects of the User model, including
    creating new users, testing the __str__ method, verifying user permissions, and
    ensuring uniqueness constraints for username, email, and phone number fields.

    Methods:
        test_create_new_user: Test case to create a new user and verify its attributes.
        test_model_str_method: Test case to verify the __str__ method of the user model.
        test_new_user_is_not_staff_or_superuser: Test case to verify that new users are not staff or superusers.
        test_username_field_is_unique: Test case to verify the uniqueness constraint for the username field.
        test_email_field_is_unique: Test case to verify the uniqueness constraint for the email field.
    """

    def test_create_new_user(self, user_factory, user_model):
        """
        Test case to create a new user and verify its attributes.

        Args:
            user_factory: Factory for creating user instances.
            user_model: The User model class.

        Assertions:
            - Asserts that a new user is created.
            - Asserts that the username is stored in lowercase.
            - Asserts that the user ID is assigned.
        """
        user = user_factory.create()

        assert user_model.objects.all().count() == 1
        assert user.username.lower() == user_model.objects.all()[0].username
        assert user.id == user_model.objects.all()[0].id

    def test_model_str_method(self, user_factory):
        """
        Test case to verify the __str__ method of the user model.

        Args:
            user_factory: Factory for creating user instances.

        Assertion:
            - Asserts that the string representation of the user is the lowercase email address.
        """
        user = user_factory.create()
        assert user.email.lower() == str(user)

    def test_new_user_is_not_superuser(self, user_factory):
        """
        Test case to verify that new users are not staff or superusers.

        Args:
            user_factory: Factory for creating user instances.

        Assertion:
            - Asserts that the is_superuser attribute is False for new users.
        """
        user = user_factory.create()
        assert not user.is_superuser

    def test_username_field_is_unique(self, user_factory, user_model):
        """
        Test case to verify the uniqueness constraint for the username field.

        Args:
            user_factory: Factory for creating user instances.
            user_model: The User model class.

        Assertion:
            - Asserts that attempting to create a user with an existing username raises an IntegrityError.
            - Asserts that the count of user objects remains unchanged.
        """
        user = user_factory.create(username="test_user_1")

        with pytest.raises(IntegrityError) as exc_info:
            user_factory.create(username="test_user_1")

        assert exc_info.type is IntegrityError
        error_message = str(exc_info.value)
        assert (
            "UNIQUE constraint failed" in error_message
            or "already exists" in error_message
        )
        assert user_model.objects.all().count() == 1

    def test_email_field_is_unique(self, user_factory, user_model):
        """
        Test case to verify the uniqueness constraint for the email field.

        Args:
            user_factory: Factory for creating user instances.
            user_model: The User model class.

        Assertion:
            - Asserts that attempting to create a user with an existing email raises an IntegrityError.
            - Asserts that the count of user objects remains unchanged.
        """
        user = user_factory.create(email="testuser@email.com")

        with pytest.raises(IntegrityError) as exc_info:
            user_factory.create(email="testuser@email.com")

        assert exc_info.type is IntegrityError
        error_message = str(exc_info.value)
        assert (
            "UNIQUE constraint failed" in error_message
            or "already exists" in error_message
        )
        assert user_model.objects.all().count() == 1