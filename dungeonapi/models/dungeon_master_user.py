from django.db import models
from dungeonapi.models import CustomUser

class DungeonMasterUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='dungeon_master_user')
    lfp_status = models.BooleanField(default=False)
