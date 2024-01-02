from django.db import models

class Race(models.Model):
    label = models.CharField(max_length=35)
    description = models.CharField(max_length=750)
    speed = models.IntegerField()
    darkvision = models.BooleanField()
    first_language = models.ForeignKey("Language", on_delete=models.CASCADE, related_name="first_language_race")
    second_language = models.ForeignKey("Language", on_delete=models.CASCADE, related_name="second_language_race")  
