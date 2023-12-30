from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from dungeonapi.models import Character, CharacterAbilityScore, CharacterSavingThrow, CharacterSkill, Background, CharacterDnDClass

class BackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Background
        fields = "__all__"

# class CharacterDnDClassSerializer(serializers.ModelSerializer):
#     dnd_class_label = serializers.CharField(source='dnd_class.label', read_only=True)

#     class Meta:
#         model = CharacterDnDClass
#         fields = ['id', 'dnd_class_label']

class CharacterAbilityScoreSerializer(serializers.ModelSerializer):
    ability_label = serializers.CharField(source='ability.label', read_only=True)
    # ability_description = serializers.CharField(source='ability.description', read_only=True)

    class Meta:
        model = CharacterAbilityScore
        fields = ['id', 'ability_id', 'score_value', 'ability_label']

class CharacterSavingThrowSerializer(serializers.ModelSerializer):
    saving_throw_label = serializers.CharField(source='saving_throw.label', read_only=True)
    # saving_throw_description =serializers.CharField(source='saving_throw.description', read_only=True)

    class Meta:
        model = CharacterSavingThrow
        fields = ['id', 'saving_throw_id', 'proficient', 'saving_throw_label']

class CharacterSkillSerializer(serializers.ModelSerializer):
    skill_label = serializers.CharField(source='skill.label', read_only=True)
    # skill_description = serializers.CharField(source='skill.description', read_only=True)

    class Meta:
        model = CharacterSkill
        fields = ['id', 'skill_id', 'proficient', 'skill_label']

class CharacterSerializer(serializers.ModelSerializer):
    background = BackgroundSerializer(read_only=True)
    user_username = serializers.CharField(source='player_user.user.username', read_only=True)
    character_abilities = CharacterAbilityScoreSerializer(many=True, read_only=True, source='characterabilityscore_set')
    character_saving_throws = CharacterSavingThrowSerializer(many=True, read_only=True, source='charactersavingthrow_set' )
    character_skills = CharacterSkillSerializer(many=True, read_only=True, source='characterskill_set')
    dnd_class_label = serializers.CharField(source='characterdndclass.dnd_class.label' ,read_only=True)

    class Meta:
        model = Character
        fields = ['id', 'player_user', 'user_username', 'dnd_class_label', 'character_name', 'level', 'race', 'sex', 'alignment', 'background', 'bio', 'notes', 'character_appearance', 'created_on', 'character_abilities', 'character_saving_throws', 'character_skills']

class CharacterViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all Characters"""
        # Retrieve the player_id from the request query parameters
        player_id = request.query_params.get('player_id', None)

        # endpoint /characters/?player_id=your_player_id
        if player_id:
            # If player_id is provided, filter characters based on it
            characters = Character.objects.filter(player_user=player_id)
        else:
            # If no player_id is provided, get all characters
            characters = Character.objects.all()

        serializer = CharacterSerializer(characters, many=True)
        return Response(serializer.data)

    def list_for_player_user(self, request, player_id=None):
        """Handle GET requests for all Characters belonging to a player"""
        try:
            characters = Character.objects.filter(player_user=player_id)
            serializer = CharacterSerializer(characters, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Character.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Character"""
        try:
            character = Character.objects.get(pk=pk)
            serializer = CharacterSerializer(character, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Character.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single Character

        Returns:
            Response -- empty response body
        """
        try:
            character = Character.objects.get(pk=pk)
            if character.player_user.user.id == request.user.id or request.user.is_staff:
                character.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            return Response({"message": "You are not the owner of this character."}, status=status.HTTP_403_FORBIDDEN)
        except Character.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 