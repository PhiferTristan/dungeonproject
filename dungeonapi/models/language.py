from django.db import models

class Language(models.Model):
    label = models.CharField(max_length=55)
    description = models.CharField(max_length=755)
    exotic = models.BooleanField(default=True)
    typical_speakers = models.CharField(max_length=155)
    script = models.CharField(max_length=35, null=True)
