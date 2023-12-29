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
