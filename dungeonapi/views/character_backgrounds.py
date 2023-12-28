from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from dungeonapi.models import Character, Background, CharacterBackground, Flaw

class BackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Background
        fields = ['id', 'label', 'languages_count']

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['id', 'character_name', 'level', 'sex', 'bio', 'notes', 'character_appearance', 'created_on', 'player_user', 'race', 'alignment']

class CharacterBackgroundSerializer(serializers.ModelSerializer):
    character = CharacterSerializer()
    background = BackgroundSerializer()

    class Meta:
        model = CharacterBackground
        fields = fields = ['id', 'character', 'background']

class CharacterBackgroundViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all Characters' Backgrounds"""
        character_backgrounds = CharacterBackground.objects.all()
        serializer = CharacterBackgroundSerializer(character_backgrounds, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Character's Background"""
        try:
            character_background = CharacterBackground.objects.get(pk=pk)
            serializer = CharacterBackgroundSerializer(character_background, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Character.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
