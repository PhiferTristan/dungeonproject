from django.db import models
from dungeonapi.models import CustomUser

class PlayerUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='player_user')
    lfg_status = models.BooleanField(default=False)
