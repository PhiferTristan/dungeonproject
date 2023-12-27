from django.db import models

class CharacterSavingThrow(models.Model):
    character = models.ForeignKey("Character", on_delete=models.CASCADE)
    saving_throw = models.ForeignKey("SavingThrow", on_delete=models.CASCADE)
    proficient = models.BooleanField()

    # class Meta:
    #     unique_together = ('character', 'saving_throw')
 