from django.db import models

class Alignment(models.Model):
    label = models.CharField(max_length=35)
    description = models.CharField(max_length=355)