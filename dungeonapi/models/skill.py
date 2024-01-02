from django.db import models

class Skill(models.Model):
    label = models.CharField(max_length=55)
    description = models.CharField(max_length=2555)
    ability = models.ForeignKey("Ability", on_delete=models.CASCADE, related_name="ability_skill")
