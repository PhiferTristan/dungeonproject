from django.db import models

class Subclass(models.Model):
    class_id = models.ForeignKey("Class", on_delete=models.CASCADE)
    label = models.CharField(max_length=55)
    description = models.CharField(max_length=1555)
    