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
        fields = ('id', 'bio', 'profile_image_url', 'created_on', 'discord_username', 'lfg_status', 'user')

class PlayerUserViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all flaws"""
        playerusers = PlayerUser.objects.all()
        serializer = PlayerUserSerializer(playerusers, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single flaw"""
        try:
            playeruser = PlayerUser.objects.get(pk=pk)
            serializer = PlayerUserSerializer(playeruser, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PlayerUser.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    # @action(detail=False, methods=['post'], url_path='register')
    # def create_player_user(self, request):

    #     serializer = PlayerUserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         custom_user_data = {
    #             'username': serializer.validated_data['username'],
    #                 'first_name': serializer.validated_data['first_name'],
    #                 'last_name': serializer.validated_data['last_name'],
    #                 'email': serializer.validated_data['email'],
    #                 'password': serializer.validated_data['password'],
    #                 'user_type': 'player'
    #         }

    #         # create a CustomUser
    #         custom_user_serializer = UserSerializer(data=custom_user_data)
    #         if custom_user_serializer.is_valid():
    #             custom_user = custom_user_serializer.save()

    #             # create a DungeonMasterUser and associate with CustomUser
    #             player_user = PlayerUser.objects.create(
    #                 user = custom_user,
    #                 created_on = serializer.validated_data['created_on'],
    #                 looking_for_group_status=serializer.validated_data['looking_for_group_status']
    #             )

    #             return Response({'message': 'Player user created successfully'}, status=status.HTTP_201_CREATED)
    #         else:
    #             return Response(custom_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 