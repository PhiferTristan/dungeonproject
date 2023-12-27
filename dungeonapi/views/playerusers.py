from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from dungeonapi.models import PlayerUser
from dungeonapi.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'user_type')

class PlayerUserSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = PlayerUser
        fields = ('id', 'lfg_status', 'user')

class PlayerUserViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all Player Users"""
        playerusers = PlayerUser.objects.all()
        serializer = PlayerUserSerializer(playerusers, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Player User"""
        try:
            playeruser = PlayerUser.objects.get(pk=pk)
            serializer = PlayerUserSerializer(playeruser, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PlayerUser.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
