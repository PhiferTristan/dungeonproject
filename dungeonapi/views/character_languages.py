from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from dungeonapi.models import Character, Language, CharacterLanguage

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'label']

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['id', 'character_name', 'level', 'sex', 'bio', 'notes', 'character_appearance', 'created_on', 'player_user', 'race', 'alignment']

class CharacterLanguageSerializer(serializers.ModelSerializer):
    character = CharacterSerializer()
    language = LanguageSerializer()

    class Meta:
        model = CharacterLanguage
        fields = fields = ['id', 'character', 'language']

class CharacterLanguageViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all Characters' Languages"""
        character_languages = CharacterLanguage.objects.all()
        serializer = CharacterLanguageSerializer(character_languages, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Character's Language"""
        try:
            character_language = CharacterLanguage.objects.get(pk=pk)
            serializer = CharacterLanguageSerializer(character_language, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Character.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
