from django.db import models

class Ability(models.Model):
    label = models.CharField(max_length=25)
    description = models.CharField(max_length=1555)
