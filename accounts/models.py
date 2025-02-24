# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model that enforces unique emails.
    """

    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
