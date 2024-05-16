"""Accounts models"""

from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy

from taskmaster.utils import BaseModel


class User(AbstractUser, BaseModel):
    """
    Custom User model representing user accounts.

    This model extends the AbstractUser class provided by Django to include additional fields
    and custom validation rules for the user's email and username.

    Attributes:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user (unique).
        username (str): The username of the user (unique).
        password (str): The hashed password of the user.
        USERNAME_FIELD (str): The field used for authentication (email).
        REQUIRED_FIELDS (list): The list of fields required during user creation (username).

    Methods:
        save(): Overrides the save method to ensure the username is always lowercase.

    Constraints:
        - The username must be at least 4 characters long.
        - The username can only contain letters, numbers, and underscores.

    Meta:
        ordering (list): The default ordering for query sets (descending date_joined).
        verbose_name (str): The human-readable name of the model.
        verbose_name_plural (str): The pluralized form of the verbose name.
        constraints (list): Additional database constraints (minimum username length).

    """

    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, blank=False, null=False)
    username = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        null=False,
        validators=[
            validators.MinLengthValidator(
                limit_value=4,
                message=gettext_lazy("Username cannot be less than 4 characters"),
            ),
            validators.RegexValidator(
                regex=r"\W",
                message=gettext_lazy(
                    "Username can only contain letters, numbers and underscore"
                ),
                inverse_match=True,
            ),
        ],
    )
    password = models.CharField(
        gettext_lazy("Password"),
        max_length=128,
        blank=True,
        null=True,
        validators=[
            validators.MinLengthValidator(limit_value=6),
        ],
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        ordering = ["-date_joined"]
        verbose_name = "User"
        verbose_name_plural = "Users"
        constraints = [
            models.CheckConstraint(
                check=models.Q(username__length__gte=4), name="min_username_length"
            ),
        ]

    def save(self, *args, **kwargs):
        """
        Override the save method to ensure the username is always lowercase.
        """
        self.username = self.username.lower()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        """
        Returns a string representation of the user object.
        """
        return self.get_username()
