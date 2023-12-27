from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from dungeonapi.models import DungeonMasterUser
from dungeonapi.models import CustomUser
from .users import UserSerializer

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'user_type')

class DungeonMasterUserSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = DungeonMasterUser
        fields = ('id', 'lfg_status', 'user')

class DungeonMasterUserViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all Dungeon Master Users"""
        dungeonmasterusers = DungeonMasterUser.objects.all()
        serializer = DungeonMasterUserSerializer(dungeonmasterusers, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Dungeon Master User"""
        try:
            dungeonmasteruser = DungeonMasterUser.objects.get(pk=pk)
            serializer = DungeonMasterUserSerializer(dungeonmasteruser, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DungeonMasterUser.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
  