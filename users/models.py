from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with location and profile information."""
    handle = models.CharField(max_length=50, unique=True, null=True, blank=True)
    photo_url = models.URLField(max_length=500, null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.handle or self.username

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['handle']),
        ]

