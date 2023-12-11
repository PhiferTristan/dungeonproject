from django.db import models

class Race(models.Model):
    label = models.CharField(max_length=35)
    description = models.CharField(max_length=750)
    speed = models.IntegerField()
