from django.db import models

class Skill(models.Model):
    label = models.CharField(max_length=55)
    description = models.CharField(max_length=2555)
