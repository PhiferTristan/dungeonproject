from django.db import models

class Background(models.Model):
    label = models.CharField(max_length=55)
    description = models.CharField(max_length=3555)
    languages_count = models.IntegerField()
    skill_prof_1 = models.ForeignKey("Skill", on_delete=models.CASCADE, related_name="skill_prof_1_skill")
    skill_prof_2 = models.ForeignKey("Skill", on_delete=models.CASCADE, related_name="skill_prof_2_skill")
