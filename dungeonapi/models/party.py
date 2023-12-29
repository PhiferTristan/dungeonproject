from django.db import models

class Party(models.Model):
    dungeon_master = models.ForeignKey("DungeonMasterUser", on_delete=models.CASCADE)
    characters = models.ManyToManyField("Character", related_name="parties")
    name = models.CharField(max_length=75)
    created_on = models.DateField(auto_now_add=True)
    lfp_status = models.BooleanField(default=False)
    description = models.CharField(max_length=755)
    