from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from dungeonapi.models import PersonalityTrait, CharacterPersonalityTrait, CharacterBackground

class PersonalityTraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalityTrait
        fields = "__all__"

class CharacterBackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterBackground
        fields = "__all__"

class CharacterPersonalityTraitSerializer(serializers.ModelSerializer):
    character_background = CharacterBackgroundSerializer()
    personality_trait = PersonalityTraitSerializer()
    class Meta:
        model = CharacterPersonalityTrait
        fields = ['id', 'character_background', 'personality_trait']


class CharacterPersonalityTraitViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all Characters' Personality Traits"""
        character_personality_traits = CharacterPersonalityTrait.objects.all()
        serializer = CharacterPersonalityTraitSerializer(character_personality_traits, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Character's Personality Trait"""
        try:
            character_personality_trait = CharacterPersonalityTrait.objects.get(pk=pk)
            serializer = CharacterPersonalityTraitSerializer(character_personality_trait, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CharacterPersonalityTrait.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
