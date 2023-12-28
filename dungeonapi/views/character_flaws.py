from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from dungeonapi.models import Flaw, CharacterFlaw, CharacterBackground

class FlawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flaw
        fields = "__all__"

class CharacterBackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterBackground
        fields = "__all__"

class CharacterFlawSerializer(serializers.ModelSerializer):
    character_background = CharacterBackgroundSerializer()
    flaw = FlawSerializer()
    class Meta:
        model = CharacterFlaw
        fields = ['id', 'character_background', 'flaw']


class CharacterFlawViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all Characters' Flaws"""
        character_flaws = CharacterFlaw.objects.all()
        serializer = CharacterFlawSerializer(character_flaws, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Character's Flaw"""
        try:
            character_flaw = CharacterFlaw.objects.get(pk=pk)
            serializer = CharacterFlawSerializer(character_flaw, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CharacterFlaw.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
