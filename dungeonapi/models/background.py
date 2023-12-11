from django.db import models

class Background(models.Model):
    label = models.CharField(max_length=55)
    description = models.CharField(max_length=3555)
    language_count = models.IntegerField()
