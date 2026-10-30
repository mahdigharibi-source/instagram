from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=14, unique=True, blank=True, null=True)
    # comments
    # liked_posts
    # posts
    # profile
    def __str__(self):
        return self.phone_number