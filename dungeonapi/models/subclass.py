from django.db import models

class Subclass(models.Model):
    dndclass = models.ForeignKey("DnDClass", on_delete=models.CASCADE)
    label = models.CharField(max_length=55)
    description = models.CharField(max_length=3555)
    