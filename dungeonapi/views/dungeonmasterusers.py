from rest_framework import viewsets
from rest_framework import serializers
from dungeonapi.models import DungeonMasterUser

class DungeonMasterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DungeonMasterUser
        fields = ('id', 'bio', 'profile_image_url', 'created_on', 'discord_username', 'lfg_status', 'user_id')

class DungeonMasterUserViewSet(viewsets.ViewSet):
    pass