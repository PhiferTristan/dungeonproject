from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from dungeonapi.models import Character, CharacterAbilityScore, CharacterSavingThrow, CharacterSkill, Background, CharacterBackground, DnDClass,CharacterDnDClass, PlayerUser, Race, Alignment, Bond, CharacterBond, Alignment, Flaw, CharacterFlaw, Ideal, CharacterIdeal, PersonalityTrait, CharacterPersonalityTrait

class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = ['label']

class AlignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alignment
        fields = ['label']

class BackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Background
        fields = "__all__"

class CharacterDnDClassSerializer(serializers.ModelSerializer):
    # dnd_class_label = serializers.CharField(source='dnd_class.label', read_only=True)
    class_id = serializers.IntegerField(source='dnd_class.dnd_class_id', read_only=True)

    class Meta:
        model = CharacterDnDClass
        fields = ['id', 'dnd_class_id', 'dnd_class_label']

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
    user_id = serializers.IntegerField(source='player_user.user.id', read_only=True)
    user_username = serializers.CharField(source='player_user.user.username', read_only=True)
    character_abilities = CharacterAbilityScoreSerializer(many=True, read_only=True, source='characterabilityscore_set')
    character_saving_throws = CharacterSavingThrowSerializer(many=True, read_only=True, source='charactersavingthrow_set' )
    character_skills = CharacterSkillSerializer(many=True, read_only=True, source='characterskill_set')
    character_bond = serializers.SerializerMethodField()
    character_flaw = serializers.SerializerMethodField()
    character_ideal = serializers.SerializerMethodField()
    character_personality_trait = serializers.SerializerMethodField()
    race_label = RaceSerializer(source='race', read_only=True)
    alignment_label = AlignmentSerializer(source='alignment', read_only=True)
    class_id = serializers.IntegerField(source='characterdndclass.dnd_class_id', read_only=True, allow_null=True)
    race_id = serializers.IntegerField(source='race.id', read_only=True, allow_null=True)
    alignment_id = serializers.IntegerField(source='alignment.id', read_only=True, allow_null=True)
    background_id = serializers.IntegerField(source='background.id', read_only=True, allow_null=True)
    class_label = serializers.CharField(source='characterdndclass.dnd_class.label' ,read_only=True)


    class Meta:
        model = Character
        fields = ['id', 'class_id', 'user_id', 'class_label', 'race_id', 'alignment_id', 'background_id', 'player_user', 'user_username', 'character_name', 'character_bond', 'character_flaw', 'character_ideal', 'character_personality_trait', 'level', 'race_label', 'sex', 'alignment_label', 'background', 'bio', 'notes', 'character_appearance', 'created_on', 'character_abilities', 'character_saving_throws', 'character_skills']


    def get_character_bond(self, obj):
        character_background = obj.get_character_background()
        if character_background:
            # Access the bond through the CharacterBond model
            character_bond = CharacterBond.objects.filter(character_background=character_background).first()
            if character_bond:
                bond = character_bond.bond
                return {
                    "id": bond.id,
                    "label": bond.label,
                    "description": bond.description,
                    "d6_number": bond.d6_number,
                }
        return None

    def get_character_flaw(self, obj):
        character_background = obj.get_character_background()
        if character_background:
            # Access the flaw through the CharacterFlaw model
            character_flaw = CharacterFlaw.objects.filter(character_background=character_background).first()
            if character_flaw:
                flaw = character_flaw.flaw
                return {
                    "id": flaw.id,
                    "label": flaw.label,
                    "description": flaw.description,
                    "d6_number": flaw.d6_number,
                }
        return None

    def get_character_ideal(self, obj):
        character_background = obj.get_character_background()
        if character_background:
            # Access the ideal through the CharacterIdeal model
            character_ideal = CharacterIdeal.objects.filter(character_background=character_background).first()
            if character_ideal:
                ideal = character_ideal.ideal
                return {
                    "id": ideal.id,
                    "label": ideal.label,
                    "description": ideal.description,
                    "d6_number": ideal.d6_number,
                }
        return None

    def get_character_personality_trait(self, obj):
        character_background = obj.get_character_background()
        if character_background:
            # Access the personality_trait through the CharacterPersonalityTrait model
            character_personality_trait = CharacterPersonalityTrait.objects.filter(character_background=character_background).first()
            if character_personality_trait:
                personality_trait = character_personality_trait.personality_trait
                return {
                    "id": personality_trait.id,
                    "label": personality_trait.label,
                    "description": personality_trait.description,
                    "d8_number": personality_trait.d8_number,
                }
        return None

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

    def create(self, request):
        """Handle POST operations for creating a new Character

        Returns:
            Response -- JSON serialized character instance
        """

        # Check if the user is a PlayerUser
        try:
            player_user = PlayerUser.objects.get(user=request.user.id)
        except PlayerUser.DoesNotExist:
            return Response({"message": "Only Players can create characters."}, status=status.HTTP_403_FORBIDDEN)

        # Extract data from the request
        character_name = request.data.get("character_name")
        level = request.data.get("level")
        race_id = request.data.get("race_id")
        sex = request.data.get("sex")
        alignment_id = request.data.get("alignment_id")
        background_id = request.data.get("background_id")
        bio = request.data.get("bio", "")
        character_appearance = request.data.get("character_appearance", "")
        notes = request.data.get("notes", "")
        bond_id = request.data.get("bond_id")
        dnd_class_id = request.data.get("dnd_class_id")

        # Fetch the Race instance based on race_id
        try:
            race = Race.objects.get(pk=race_id)
        except Race.DoesNotExist:
            return Response({"message": f"Race with ID {race_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the Alignment instance based on alignment_id
        try:
            alignment = Alignment.objects.get(pk=alignment_id)
        except Alignment.DoesNotExist:
            return Response({"message": f"Alignment with ID {alignment_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the Background instance based on background_id
        try:
            background = Background.objects.get(pk=background_id)
        except Background.DoesNotExist:
            return Response({"message": f"Background with ID {background_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the DnDClass instance based on dnd_class_id
        try:
            dnd_class = DnDClass.objects.get(pk=dnd_class_id)
        except DnDClass.DoesNotExist:
            return Response({"message": f"DnDClass with ID {dnd_class_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)


        # Create a new character
        character = Character.objects.create(
            player_user=player_user,
            character_name=character_name,
            level=level,
            race=race,
            sex=sex,
            alignment=alignment,
            background=background,
            bio=bio,
            character_appearance=character_appearance,
            notes=notes
        )

         # Create CharacterDnDClass instance
        character_dnd_class = CharacterDnDClass.objects.create(
            character=character,
            dnd_class=dnd_class
        )

        character_background = CharacterBackground.objects.create(
            character=character,
            background=background
        )

        # Fetch the bond_id from the request
        bond_id = request.data.get("bond_id")

        # If a bond_id is provided, create a CharacterBond instance
        if bond_id:
            try:
                bond = Bond.objects.get(pk=bond_id)
            except Bond.DoesNotExist:
                return Response({"message": f"Bond with ID {bond_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            # Create a CharacterBond instance
            character_bond = CharacterBond.objects.create(
                bond=bond,
                character_background=character_background
            )

        # Fetch the flaw_id from the request
        flaw_id = request.data.get("flaw_id")

        # If a flaw_id is provided, create a CharacterFlaw instance
        if flaw_id:
            try:
                flaw = Flaw.objects.get(pk=flaw_id)
            except Flaw.DoesNotExist:
                return Response({"message": f"Flaw with ID {flaw_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            # Create a CharacterFlaw instance
            character_flaw = CharacterFlaw.objects.create(
                flaw=flaw,
                character_background=character_background
            )

        # Fetch the ideal_id from the request
        ideal_id = request.data.get("ideal_id")

        # If a ideal_id is provided, create a CharacterIdeal instance
        if ideal_id:
            try:
                ideal = Ideal.objects.get(pk=ideal_id)
            except Ideal.DoesNotExist:
                return Response({"message": f"Ideal with ID {ideal_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            # Create a CharacterIdeal instance
            character_ideal = CharacterIdeal.objects.create(
                ideal=ideal,
                character_background=character_background
            )

        # Fetch the personality_trait_id from the request
        personality_trait_id = request.data.get("personality_trait_id")

        # If a personality_trait_id is provided, create a CharacterPersonalityTrait instance
        if personality_trait_id:
            try:
                personality_trait = PersonalityTrait.objects.get(pk=personality_trait_id)
            except PersonalityTrait.DoesNotExist:
                return Response({"message": f"Personality Trait with ID {personality_trait_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            # Create a CharacterPersonalityTrait instance
            character_personality_trait = CharacterPersonalityTrait.objects.create(
                personality_trait=personality_trait,
                character_background=character_background
            )

        # Extract ability scores from request data
        ability_scores = request.data.get("ability_scores", {})

        # Create CharacterAbilityScore instances for each ability
        for ability_id, score_value in ability_scores.items():
            CharacterAbilityScore.objects.create(
                character=character,
                ability_id=ability_id,
                score_value=score_value
            )

        character.created_on = character.created_on.strftime("%m-%d-%Y")

        # Serialize the character and return the response
        try:
            serializer = CharacterSerializer(character, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT operations for updating a Character

        Returns:
            Response -- JSON serialized updated character instance
        """

        # Fetch the existing character instance
        character = get_object_or_404(Character, pk=pk)

        # Your existing logic for checking if the user is a PlayerUser can be reused here

        # Extract data from the request (similar to the create method)
        character_name = request.data.get("character_name", character.character_name)
        level = request.data.get("level", character.level)
        race_id = request.data.get("race_id", character.race_id)
        sex = request.data.get("sex", character.sex)
        alignment_id = request.data.get("alignment_id", character.alignment_id)
        background_id = request.data.get("background_id", character.background_id)
        bio = request.data.get("bio", character.bio)
        character_appearance = request.data.get("character_appearance", character.character_appearance)
        notes = request.data.get("notes", character.notes)
        bond_id = request.data.get("bond_id", None)
        flaw_id = request.data.get("flaw_id", None)
        ideal_id = request.data.get("ideal_id", None)
        personality_trait_id = request.data.get("personality_trait_id", None)
        dnd_class_id = request.data.get("dnd_class_id", character.characterdndclass.dnd_class_id)

        # Fetch the Race instance based on race_id
        try:
            race = Race.objects.get(pk=race_id)
        except Race.DoesNotExist:
            return Response({"message": f"Race with ID {race_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the Alignment instance based on alignment_id
        try:
            alignment = Alignment.objects.get(pk=alignment_id)
        except Alignment.DoesNotExist:
            return Response({"message": f"Alignment with ID {alignment_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the Background instance based on background_id
        try:
            background = Background.objects.get(pk=background_id)
        except Background.DoesNotExist:
            return Response({"message": f"Background with ID {background_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the DnDClass instance based on dnd_class_id
        try:
            dnd_class = DnDClass.objects.get(pk=dnd_class_id)
        except DnDClass.DoesNotExist:
            return Response({"message": f"DnDClass with ID {dnd_class_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)


        # Update the existing character instance
        character.character_name = character_name
        character.level = level
        character.race = race
        character.sex = sex
        character.alignment = alignment
        character.background = background
        character.bio = bio
        character.character_appearance = character_appearance
        character.notes = notes

        # Save the updated character instance
        character.save()

        # Update CharacterDnDClass instance
        character_dnd_class = character.characterdndclass
        character_dnd_class.dnd_class = dnd_class
        character_dnd_class.save()

        # Fetch the existing character_background instance
        character_background = character.get_character_background()

        # Your existing logic for creating/updating CharacterBond, CharacterFlaw, etc., can be reused here
        # Fetch the bond_id from the request
        bond_id = request.data.get("bond_id")

        # Update or create CharacterBond instance
        if bond_id:
            try:
                bond = Bond.objects.get(pk=bond_id)
            except Bond.DoesNotExist:
                return Response({"message": f"Bond with ID {bond_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if a CharacterBond instance already exists
            character_bond, created = CharacterBond.objects.get_or_create(
                character_background=character_background,
                defaults={"bond": bond}
            )

            # If not created, update the bond
            if not created:
                character_bond.bond = bond
                character_bond.save()

        # Update or create CharacterFlaw instance
        if flaw_id:
            try:
                flaw = Flaw.objects.get(pk=flaw_id)
            except Flaw.DoesNotExist:
                return Response({"message": f"Flaw with ID {flaw_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if a CharacterFlaw instance already exists
            character_flaw, created = CharacterFlaw.objects.get_or_create(
                character_background=character_background,
                defaults={"flaw": flaw}
            )

            # If not created, update the flaw
            if not created:
                character_flaw.flaw = flaw
                character_flaw.save()

        # Update or create CharacterIdeal instance
        if ideal_id:
            try:
                ideal = Ideal.objects.get(pk=ideal_id)
            except Ideal.DoesNotExist:
                return Response({"message": f"Ideal with ID {ideal_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if a CharacterIdeal instance already exists
            character_ideal, created = CharacterIdeal.objects.get_or_create(
                character_background=character_background,
                defaults={"ideal": ideal}
            )

            # If not created, update the ideal
            if not created:
                character_ideal.ideal = ideal
                character_ideal.save()

        # Update or create CharacterPersonalityTrait instance
        if personality_trait_id:
            try:
                personality_trait = PersonalityTrait.objects.get(pk=personality_trait_id)
            except PersonalityTrait.DoesNotExist:
                return Response({"message": f"Personlaity Trait with ID {personality_trait_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if a CharacterPersonalityTrait instance already exists
            character_personality_trait, created = CharacterPersonalityTrait.objects.get_or_create(
                character_background=character_background,
                defaults={"personality_trait": personality_trait}
            )

            # If not created, update the personality_trait
            if not created:
                character_personality_trait.personality_trait = personality_trait
                character_personality_trait.save()

        # Update ability scores from request data
        ability_scores = request.data.get("ability_scores", {})

        for ability_id, score_value in ability_scores.items():
            # Get or create CharacterAbilityScore instance
            character_ability_score, created = CharacterAbilityScore.objects.get_or_create(
                character=character,
                ability_id=ability_id,
                defaults={"score_value": score_value}
            )

            # If not created, update the score_value
            if not created:
                character_ability_score.score_value = score_value
                character_ability_score.save()

        # Serialize the character and return the response
        try:
            serializer = CharacterSerializer(character, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
