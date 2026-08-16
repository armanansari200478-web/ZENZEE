from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model for ZENZEE Fashion Platform.
    Inherits standard Django auth (username, email, password, first_name, last_name)
    and adds custom attributes needed for youth fashion profile management.
    """
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.email})"
