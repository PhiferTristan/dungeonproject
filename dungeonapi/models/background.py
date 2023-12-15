from django.db import models

class Background(models.Model):
    label = models.CharField(max_length=55)
    description = models.CharField(max_length=3555)
    languages_count = models.IntegerField()
