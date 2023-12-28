from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from dungeonapi.models import Character, Ability, CharacterAbilityScore

class AbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ability
        fields = "__all__"

class CharacterAbilityScoreSerializer(serializers.ModelSerializer):
    ability = AbilitySerializer()

    class Meta:
        model = CharacterAbilityScore
        fields = fields = ['id', 'character_id', 'ability_id', 'score_value', 'ability']

class CharacterAbilityScoreViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all Character's Ability Scores"""
        character_ability_scores = CharacterAbilityScore.objects.all()
        serializer = CharacterAbilityScoreSerializer(character_ability_scores, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Character's Ability Score"""
        try:
            character_ability_score = CharacterAbilityScore.objects.get(pk=pk)
            serializer = CharacterAbilityScoreSerializer(character_ability_score, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Character.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
