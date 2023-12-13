from django.db import models

class Bond(models.Model):
    label = models.CharField(max_length=75)
    description = models.CharField(max_length=1555)
    background = models.ForeignKey("Background", on_delete=models.CASCADE)
    d6_number = models.IntegerField()