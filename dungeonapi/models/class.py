from django.db import models

class Class(models.Model):
    label = models.CharField(max_length=55)
    description = models.CharField(max_length=1555)
    # subclass = models.ForeignKey("Subclass", on_delete=models.CASCADE)