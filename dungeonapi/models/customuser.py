from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('DM', 'Dungeon Master'),
        ('Player', 'Player')
    ]

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='Player')

    bio = models.CharField(max_length=355)
    profile_image_url = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=255)
    discord_username = models.CharField(max_length=55)

    def __str__(self):
        return self.username
    