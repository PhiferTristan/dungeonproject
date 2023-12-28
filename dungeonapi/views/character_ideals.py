from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from dungeonapi.models import Ideal, CharacterIdeal, CharacterBackground

class IdealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ideal
        fields = "__all__"

class CharacterBackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterBackground
        fields = "__all__"

class CharacterIdealSerializer(serializers.ModelSerializer):
    character_background = CharacterBackgroundSerializer()
    ideal = IdealSerializer()
    class Meta:
        model = CharacterIdeal
        fields = ['id', 'character_background', 'ideal']


class CharacterIdealViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all Characters' Ideals"""
        character_ideals = CharacterIdeal.objects.all()
        serializer = CharacterIdealSerializer(character_ideals, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Character's Ideal"""
        try:
            character_ideal = CharacterIdeal.objects.get(pk=pk)
            serializer = CharacterIdealSerializer(character_ideal, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CharacterIdeal.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
