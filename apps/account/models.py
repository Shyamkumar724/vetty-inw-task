from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import EmailValidator


class Account(AbstractUser):
    email = models.EmailField(
        unique=True,
        max_length=50,
        validators=[EmailValidator()],
    )
    groups = models.ManyToManyField(
        Group,
        related_name="account_groups",
        blank=True,
        help_text=(
            "The groups this user belongs to."
            "A user will get all permissions granted to each of their groups."
        ),
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="account_user_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
