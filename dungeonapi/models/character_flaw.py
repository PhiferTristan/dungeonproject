from django.db import models

class CharacterFlaw(models.Model):
    # character = models.ForeignKey("Character", on_delete=models.CASCADE)
    # background = models.ForeignKey("Background", on_delete=models.CASCADE)
    character_background = models.ForeignKey("CharacterBackground", on_delete=models.CASCADE)
    flaw = models.ForeignKey("Flaw", on_delete=models.CASCADE)
