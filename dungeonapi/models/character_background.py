from django.db import models

class CharacterBackground(models.Model):
    character = models.ForeignKey("Character", on_delete=models.CASCADE)
    background = models.ForeignKey("Background", on_delete=models.CASCADE)
 