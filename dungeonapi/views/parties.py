from django.db.models import Q
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from dungeonapi.models import Party, DungeonMasterUser, Character, CustomUser, PlayerUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username')

class DungeonMasterUserSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = DungeonMasterUser
        fields = "__all__"

class PlayerUserSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = PlayerUser
        fields = "__all__"

class CharacterSerializer(serializers.ModelSerializer):
    player_user = PlayerUserSerializer()

    class Meta:
        model = Character
        fields = ['id', 'character_name', 'level', 'player_user', 'race', 'current_party']

class PartySerializer(serializers.ModelSerializer):
    dungeon_master = DungeonMasterUserSerializer()
    characters = CharacterSerializer(many=True)

    class Meta:
        model = Party
        fields = ['id', 'name', 'created_on', 'lfp_status', 'description', 'dungeon_master', 'characters']

class PartyViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all Parties"""
        # Retrieve the player_id and dungeon_master_id from the request query parameters
        player_id = request.query_params.get('player_id', None)
        dungeon_master_id = request.query_params.get('dungeon_master_id', None)

        # endpoint /parties/?player_id=your_player_id&dungeon_master_id=your_dm_id
        if player_id or dungeon_master_id:
            # If either player_id or dungeon_master_id is provided, filter parties based on either
            parties = Party.objects.filter(
                Q(characters__player_user=player_id) | Q(dungeon_master__user=dungeon_master_id)
            ).distinct()
        else:
            # If neither player_id nor dungeon_master_id is provided, get all parties
            parties = Party.objects.all()

        serializer = PartySerializer(parties, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def list_for_player_user(self, request, pk=None):
        """Handle GET requests for all Parties a player_user is a part of"""
        try:
            # player_user = PlayerUser.objects.get(user=request.user)
            player_user = PlayerUser.objects.get(pk=pk)
            parties = Party.objects.filter(characters__player_user=player_user)
            serializer = PartySerializer(parties, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PlayerUser.DoesNotExist as ex:
            return Response({"message": "User is not a player user"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def list_for_dungeon_master_user(self, request, pk=None):
        """Handle GET requests for all Parties a dungeon_master_user is a part of"""
        try:
            dungeon_master_user = DungeonMasterUser.objects.get(pk=pk)
            parties = Party.objects.filter(dungeon_master=dungeon_master_user)
            serializer = PartySerializer(parties, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DungeonMasterUser.DoesNotExist as ex:
            return Response({"message": "Dungeon master user not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Party"""
        try:
            party = Party.objects.get(pk=pk)
            serializer = PartySerializer(party, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Party.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single Party

        Returns:
            Response -- empty response body
        """
        try:
            party = Party.objects.get(pk=pk)
            if party.dungeon_master.user.id == request.user.id:
                party.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            return Response({"message": "You are not the DM of this party."}, status=status.HTTP_403_FORBIDDEN)
        except Party.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle PUT requests for a single post

        Returns:
            Response -- JSON serialized object
        """
        try:
            party = Party.objects.get(pk=pk)

            # This is handling the image
            # format, imgstr = request.data["image_url"].split(';base64,')
            # ext = format.split('/')[-1]
            # data = ContentFile(base64.b64decode(imgstr), name=f'{pk}-{uuid.uuid4()}.{ext}')

            if party.dungeon_master.user.id == request.user.id:
                serializer = PartySerializer(data=request.data, partial=True)
                if serializer.is_valid():
                    party.name = serializer.validated_data["name"]
                    party.description = serializer.validated_data["description"]
                    party.lfp_status = serializer.validated_data["lfp_status"]
                    party.save()

                    serializer = PartySerializer(party, context={"request": request})
                    return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "You are not the DM of this party."}, status=status.HTTP_403_FORBIDDEN)
        except Party.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized post instance
        """

        try:
            dungeon_master = DungeonMasterUser.objects.get(user=request.user.id)
        except DungeonMasterUser.DoesNotExist:
            return Response({"message": "Only Dungeon Masters can create parties."}, status=status.HTTP_403_FORBIDDEN)

        # dungeon_master = DungeonMasterUser.objects.get(user=request.user.id)
        name = request.data.get("name")
        description = request.data.get("description")
        lfp_status = request.data.get("lfp_status")

        party = Party.objects.create(
            dungeon_master = dungeon_master,
            name = name,
            description = description,
            lfp_status = lfp_status,
        )

        party.created_on = party.created_on.strftime("%m-%d-%Y")

        try:
            serializer = PartySerializer(party, context={"request": request} )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(ex, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def remove_character(self, request, pk=None, character_id=None):
        """Handle DELETE requests to remove a Character from a Party"""
        # url pattern: /parties/{party_id}/remove_player/{character_id}/
        try:
            party = Party.objects.get(pk=pk)
            character_id = self.kwargs.get('character_id')
            print(f'Party: {party}, Character Id: {character_id}')

            # Ensure that the User making the request is the Dungeon Master
            if party.dungeon_master.user.id == request.user.id:            
                # Find the Character in the Party's Characters and remove it
                character = party.characters.filter(id=character_id).first()
                if character:
                    party.characters.remove(character)
                    party.save()
                    return Response({"message": f"Character removed from party {pk}"}, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({"message": "Character not found in party"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "You are not the DM of this party."}, status=status.HTTP_403_FORBIDDEN)
        except Party.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['delete'])
    def leave_party(self, request, pk=None, character_id=None):
        """Handle DELETE requests for a Player User's Character to leave a Party"""
        try:
            party = Party.objects.get(pk=pk)
            player_user = PlayerUser.objects.get(user=request.user)

            # Check if the Player User is a member of the Party
            if party.characters.filter(id=character_id, player_user=player_user).exists():
                # Remove the Character from the Party
                character = party.characters.get(id=character_id, player_user=player_user)
                party.characters.remove(character)
                party.save()
                return Response({"message": "Player's character has left the party"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "Player's character is not a member of this party or character not found"}, status=status.HTTP_400_BAD_REQUEST)

        except Party.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except PlayerUser.DoesNotExist as ex:
            return Response({"message": "User is not a player user"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['put'])
    def add_character(self, request, pk=None):
        """Handle PUT requests to add an existing Character to a Party"""
        try:
            party = Party.objects.get(pk=pk)

            # Check if the user making the request is a player user
            try:
                player_user = PlayerUser.objects.get(user=request.user)
            except PlayerUser.DoesNotExist:
                return Response({"message": "Only Player Users can add characters to parties."}, status=status.HTTP_403_FORBIDDEN)

            # Get the character_id from the request data
            character_id = request.data.get("character_id")
            if not character_id:
                return Response({"message": "Character ID is required in the request body."}, status=status.HTTP_400_BAD_REQUEST)

            # Get the existing character
            character = Character.objects.get(id=character_id, player_user=player_user)

            # Add the character to the party
            party.characters.add(character)
            party.save()

            # Return the serialized character and party
            character_serializer = CharacterSerializer(character, context={"request": request})
            party_serializer = PartySerializer(party, context={"request": request})
            return Response({"character": character_serializer.data, "party": party_serializer.data}, status=status.HTTP_200_OK)

        except Party.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Character.DoesNotExist as ex:
            return Response({"message": "Character not found or doesn't belong to the user."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        