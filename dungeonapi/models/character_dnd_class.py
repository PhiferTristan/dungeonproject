from django.db import models

class CharacterDnDClass(models.Model):
    character = models.OneToOneField("Character", on_delete=models.CASCADE)
    dnd_class = models.ForeignKey("DnDClass", on_delete=models.CASCADE)
