from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from dungeonapi.models import PlayerUser, CustomUser, Character, Race, DnDClass

class DnDClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = DnDClass
        fields = ['label']

class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = ['label']

class CharacterSerializer(serializers.ModelSerializer):
    class_label = serializers.CharField(source='characterdndclass.dnd_class.label' ,read_only=True)
    race_label = RaceSerializer(source='race', read_only=True)
    class Meta:
        model = Character
        fields = ['id', 'race_label', 'class_label', 'character_name', 'level', 'created_on', 'player_user', 'race', 'alignment', 'background']

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'user_type')

class PlayerUserSerializer(serializers.ModelSerializer):
    characters = CharacterSerializer(many=True)
    user = CustomUserSerializer()

    class Meta:
        model = PlayerUser
        fields = ('id', 'lfg_status', 'user', 'characters')

class PlayerUserViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all Player Users"""
        player_users = PlayerUser.objects.all()
        serializer = PlayerUserSerializer(player_users, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Player User"""
        try:
            player_user = PlayerUser.objects.get(pk=pk)
            serializer = PlayerUserSerializer(player_user, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PlayerUser.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
