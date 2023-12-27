from django.db import models

class CharacterSkill(models.Model):
    character = models.ForeignKey("Character", on_delete=models.CASCADE)
    skill = models.ForeignKey("Skill", on_delete=models.CASCADE)
    proficient = models.BooleanField()

    # class Meta:
    #     unique_together = ('character', 'skill')
              