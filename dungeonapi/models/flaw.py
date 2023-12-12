from django.db import models

class Flaw(models.Model):
    label = models.CharField(max_length=75)
    description = models.CharField(max_length=1555)
