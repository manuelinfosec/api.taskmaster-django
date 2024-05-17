"""Test factories"""

import factory
import factory.fuzzy
from django.contrib.auth import get_user_model
from faker import Faker

from taskmanager.models import Task


fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory class for creating user instances.

    This factory class provides a convenient way to generate user instances for testing purposes.
    It automatically generates random values for user attributes such as first name, last name, username,
    email, and password.

    Attributes:
        first_name: A fake first name generated using Faker.
        last_name: A fake last name generated using Faker.
        username: A unique username generated using Faker with a sequence number appended to ensure uniqueness.
        email: A unique email address generated using Faker with a sequence number appended to ensure uniqueness.
        password: A randomly generated password using Faker.

    Methods:
        _create: Overrides the default create method to set the password using set_password() before saving the user instance.
    """

    class Meta:
        model = get_user_model()

    first_name = fake.first_name()
    last_name = fake.last_name()
    username = factory.Sequence(lambda x: f"{fake.user_name()}_{x}")
    email = factory.Sequence(lambda x: f"{fake.user_name()}_{x}@email.com")
    password = fake.password(length=8)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Create method to set the password using set_password() before saving the user instance.

        Args:
            model_class: The user model class.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            obj: The created user instance.
        """
        obj = model_class(*args, **kwargs)
        obj.set_password(kwargs["password"])
        obj.save()
        return obj


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    user = factory.SubFactory(UserFactory)
    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph")
    status_task = "TO DO"
