from django.db import models

class CharacterAbilityScore(models.Model):
    character = models.ForeignKey("Character", on_delete=models.CASCADE)
    ability = models.ForeignKey("Ability", on_delete=models.CASCADE)
    score_value = models.IntegerField()

    # class Meta:
    #     unique_together = ('character', 'ability')
    