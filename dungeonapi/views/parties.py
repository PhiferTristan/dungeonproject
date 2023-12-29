from rest_framework import viewsets, status, serializers
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
        fields = ['id', 'character_name', 'level', 'player_user']

class PartySerializer(serializers.ModelSerializer):
    dungeon_master = DungeonMasterUserSerializer()
    characters = CharacterSerializer(many=True)

    class Meta:
        model = Party
        fields = ['id', 'name', 'created_on', 'lfp_status', 'description', 'dungeon_master', 'characters']

class PartyViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all Parties"""
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
