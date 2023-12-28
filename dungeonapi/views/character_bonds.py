from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from dungeonapi.models import Bond, CharacterBond, CharacterBackground

class BondSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bond
        fields = "__all__"

class CharacterBackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterBackground
        fields = "__all__"

class CharacterBondSerializer(serializers.ModelSerializer):
    character_background = CharacterBackgroundSerializer()
    bond = BondSerializer()
    class Meta:
        model = CharacterBond
        fields = ['id', 'character_background', 'bond']


class CharacterBondViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all Characters' Bonds"""
        character_bonds = CharacterBond.objects.all()
        serializer = CharacterBondSerializer(character_bonds, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Character's Bond"""
        try:
            character_bond = CharacterBond.objects.get(pk=pk)
            serializer = CharacterBondSerializer(character_bond, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CharacterBond.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
