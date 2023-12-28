from django.db import models

class SavingThrow(models.Model):
    label = models.CharField(max_length=55)
    description = models.CharField(max_length=355)
    