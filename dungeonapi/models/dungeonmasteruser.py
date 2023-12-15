from django.db import models
from django.contrib.auth.models import User

class DungeonMasterUser(models.Model):
    bio = models.CharField(max_length=355)
    profile_image_url = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=155)
    created_on = models.DateField(auto_now_add=True)
    discord_username = models.CharField(max_length=55)
    lfg_status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dungeon_master_user')