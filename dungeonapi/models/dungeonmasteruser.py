from django.db import models
from dungeonapi.models import CustomUser

class DungeonMasterUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='dungeon_master_user')
    bio = models.CharField(max_length=355)
    profile_image_url = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=155)
    created_on = models.DateField(auto_now_add=True)
    discord_username = models.CharField(max_length=55)
    lfg_status = models.BooleanField(default=False)