from django.db import models

class Class(models.Model):
    label = models.CharField(max_length=55)
    description = models.CharField(max_length=1555)
    hit_die = models.IntegerField()
    primary_ability = models.CharField(max_length=35)
    saving_throw_prof_1 = models.ForeignKey("Saving Throw Proficiency", on_delete=models.CASCADE)
    saving_throw_prof_2 = models.ForeignKey("Saving Throw Proficiency", on_delete=models.CASCADE)
