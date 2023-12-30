from django.db import models
from django.contrib.auth.models import User

class Character(models.Model):
    player_user = models.ForeignKey("PlayerUser", on_delete=models.CASCADE, related_name='characters')
    character_name = models.CharField(max_length=55)
    level = models.IntegerField()
    race = models.ForeignKey("Race", on_delete=models.CASCADE)
    sex = models.CharField(max_length=35)
    alignment = models.ForeignKey("Alignment", on_delete=models.CASCADE)
    background = models.ForeignKey("Background", on_delete=models.CASCADE)
    bio = models.CharField(max_length=755)
    notes = models.CharField(max_length=755)
    character_appearance = models.CharField(max_length=755)
    created_on = models.DateField(auto_now_add=True)
    character_abilities = models.ManyToManyField("Ability", through='CharacterAbilityScore')
    character_saving_throws = models.ManyToManyField("SavingThrow", through='CharacterSavingThrow')
    character_skills = models.ManyToManyField("Skill", through='CharacterSkill')
    current_party = models.ForeignKey("Party", null=True, blank=True, on_delete=models.SET_NULL)
    character_languages = models.ManyToManyField("Language", through='CharacterLanguage')

    def get_character_background(self):
        return self.characterbackground_set.first()
