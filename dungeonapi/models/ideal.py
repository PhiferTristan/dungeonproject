from django.db import models

class Ideal(models.Model):
    label = models.CharField(max_length=75)
    description = models.CharField(max_length=755)
    alignment_group = models.CharField(max_length=35)
    background = models.ForeignKey("Background", on_delete=models.CASCADE)
    d6_number = models.IntegerField()
