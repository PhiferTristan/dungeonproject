from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from dungeonapi.models import Character, CharacterAbilityScore, CharacterSavingThrow, CharacterSkill

class CharacterAbilityScoreSerializer(serializers.ModelSerializer):
    ability_label = serializers.CharField(source='ability.label', read_only=True)
    ability_description = serializers.CharField(source='ability.description', read_only=True)

    class Meta:
        model = CharacterAbilityScore
        fields = ['id', 'character_id', 'ability_id', 'score_value', 'ability_label', 'ability_description']

class CharacterSavingThrowSerializer(serializers.ModelSerializer):
    saving_throw_label = serializers.CharField(source='saving_throw.label', read_only=True)
    saving_throw_description =serializers.CharField(source='saving_throw.description', read_only=True)

    class Meta:
        model = CharacterSavingThrow
        fields = ['id', 'character_id', 'saving_throw_id', 'proficient', 'saving_throw_label', 'saving_throw_description']

class CharacterSkillSerializer(serializers.ModelSerializer):
    skill_label = serializers.CharField(source='skill.label', read_only=True)
    skill_description = serializers.CharField(source='skill.description', read_only=True)

    class Meta:
        model = CharacterSkill
        fields = ['id', 'character_id', 'skill_id', 'proficient', 'skill_label', 'skill_description']

class CharacterSerializer(serializers.ModelSerializer):
    character_abilities = CharacterAbilityScoreSerializer(many=True, read_only=True, source='characterabilityscore_set')
    character_saving_throws = CharacterSavingThrowSerializer(many=True, read_only=True, source='charactersavingthrow_set' )
    character_skills = CharacterSkillSerializer(many=True, read_only=True, source='characterskill_set')

    class Meta:
        model = Character
        fields = ['id', 'player_user', 'character_name', 'level', 'race', 'sex', 'alignment', 'background', 'bio', 'notes', 'character_appearance', 'created_on', 'character_abilities', 'character_saving_throws', 'character_skills']

class CharacterViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all Characters"""
        characters = Character.objects.all()
        serializer = CharacterSerializer(characters, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Character"""
        try:
            character = Character.objects.get(pk=pk)
            serializer = CharacterSerializer(character, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Character.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)