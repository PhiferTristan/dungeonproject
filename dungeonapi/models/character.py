from django.db import models
from django.contrib.auth.models import User

class Character(models.Model):
    player_user = models.ForeignKey("PlayerUser", on_delete=models.CASCADE, related_name='player')
    character_name = models.CharField(max_length=55)
    level = models.IntegerField()
    # race = models.ForeignKey("Race", on_delete=models.CASCADE)
    # sex = models.CharField(max_length=35)
    # alignment = models.ForeignKey("Alignment", on_delete=models.CASCADE)
    # background = models.ForeignKey("Background", on_delete=models.CASCADE)
    # ability_scores_table = models.ForeignKey("Ability_Scores", on_delete=models.CASCADE)
    # skills_table = models.ForeignKey("Skills", on_delete=models.CASCADE)
    # saving_throws_table = models.ForeignKey("Saving_Throws", on_delete=models.CASCADE)
    # bio = models.CharField(max_length=755)
    notes = models.CharField(max_length=755)
    character_appearance = models.CharField(max_length=755)
    created_on = models.DateField(auto_now_add=True)
