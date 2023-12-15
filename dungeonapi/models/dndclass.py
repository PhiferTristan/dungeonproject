from django.db import models

class DnDClass(models.Model):
    label = models.CharField(max_length=55)
    description = models.CharField(max_length=1555)
    hit_die = models.IntegerField()
    primary_ability = models.CharField(max_length=35)
    saving_throw_prof_1 = models.ForeignKey("SavingThrow", on_delete=models.CASCADE, related_name="saving_throw_prof_1")
    saving_throw_prof_2 = models.ForeignKey("SavingThrow", on_delete=models.CASCADE, related_name="saving_throw_prof_2")
