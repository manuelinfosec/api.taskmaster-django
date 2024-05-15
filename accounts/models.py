from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy

from taskmaster.utils import BaseModel


class User(AbstractUser, BaseModel):

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
        self.username = self.username.lower()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.get_username()
