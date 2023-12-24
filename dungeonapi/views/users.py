from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from dungeonapi.models import PlayerUser, DungeonMasterUser
from dungeonapi.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password', 'user_type', 'bio', 'discord_username', 'profile_image_url')
        extra_kwargs = {'password': {'write_only': True}}

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
                'id': token.user.id
            }

            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='login')
    def login_user(self, request):
        '''Handles the authentication of a user

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
                'id': token.user.id
            }
            return Response(data)
        else:
            # Bad login details were provided. So we can't log the user in.
            data = { 'valid': False }
            return Response(data)
        