from rest_framework import viewsets
from rest_framework import serializers
from dungeonapi.models import PlayerUser

class PlayerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerUser
        fields = ('id', 'bio', 'profile_image_url', 'created_on', 'discord_username', 'lfg_status', 'user_id')

class PlayerUserViewSet(viewsets.ViewSet):
    pass