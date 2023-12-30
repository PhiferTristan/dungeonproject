from django.db import models

class CharacterLanguage(models.Model):
    character = models.ForeignKey("Character", on_delete=models.CASCADE)
    language = models.ForeignKey("Language", on_delete=models.CASCADE)
    # background = models.ForeignKey("Background", on_delete=models.CASCADE)
    # character_background = models.ForeignKey("CharacterBackground", on_delete=models.CASCADE)
