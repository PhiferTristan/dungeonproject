from django.db import models

class CharacterPersonalityTrait(models.Model):
    # character = models.ForeignKey("Character", on_delete=models.CASCADE)
    # background = models.ForeignKey("Background", on_delete=models.CASCADE)
    character_background = models.ForeignKey("CharacterBackground", on_delete=models.CASCADE)
    personality_trait = models.ForeignKey("PersonalityTrait", on_delete=models.CASCADE)
