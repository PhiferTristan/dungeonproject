from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('DM', 'Dungeon Master'),
        ('Player', 'Player')
    ]

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='Player')

    bio = models.CharField(max_length=355, blank=True)
    profile_image_url = models.URLField(max_length=255, blank=True)
    discord_username = models.CharField(max_length=55, blank=True)

    def __str__(self):
        return self.username
    