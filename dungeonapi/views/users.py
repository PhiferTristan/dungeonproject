from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from dungeonapi.models import PlayerUser, DungeonMasterUser
from dungeonapi.models import CustomUser

class DungeonMasterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DungeonMasterUser
        fields = ['lfp_status']

class PlayerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerUser
        fields = ['lfg_status']

class UserSerializer(serializers.ModelSerializer):
    dungeon_master_user = DungeonMasterUserSerializer(read_only=True)
    player_user = PlayerUserSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password', 'user_type', 'bio', 'discord_username', 'profile_image_url', 'dungeon_master_user', 'player_user')
        extra_kwargs = {'password': {'write_only': True}}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_type = data.get('user_type')

        if user_type == 'DM':
            data.pop('player_user')
        elif user_type == 'Player':
            data.pop('dungeon_master_user')

        return data

class UserViewSet(viewsets.ViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'], url_path='register')
    def register_account(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():

            user = CustomUser.objects.create_user(
                username=serializer.validated_data['username'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                user_type=serializer.validated_data.get('user_type', 'Player'),
                bio=serializer.validated_data.get('bio', ''),
                discord_username=serializer.validated_data.get('discord_username', ''),
                profile_image_url=serializer.validated_data.get('profile_image_url', '')
            )

            if user.user_type == 'DM':
                DungeonMasterUser.objects.create(user=user)
            else:
                PlayerUser.objects.create(user=user)

            token, created = Token.objects.get_or_create(user=user)

            data = {
                'valid': True,
                'token': token.key,
                'staff': token.user.is_staff,
                'id': token.user.id,
                'user_type': token.user.user_type
            }

            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='login')
    def login_user(self, request):
        '''Handles the authentication of a User

        Method arguments:
        request -- The full HTTP request object
        '''
        username = request.data['username']
        password = request.data['password']

        # Use the built-in authenticate method to verify
        # authenticate returns the user object or None if no user is found
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, respond with their token
        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)

            data = {
                'valid': True,
                'token': token.key,
                'staff': token.user.is_staff,
                'id': token.user.id,
                'user_type': token.user.user_type
            }
            return Response(data)
        else:
            # Bad login details were provided. So we can't log the user in.
            data = { 'valid': False }
            return Response(data)

    def list(self, request):
        """Handle GET requests for all Users"""
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single User"""
        try:
            user = CustomUser.objects.get(pk=pk)
            serializer = UserSerializer(user, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        