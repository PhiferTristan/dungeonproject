from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from dungeonapi.models import Character, SavingThrow, CharacterSavingThrow

class SavingThrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingThrow
        fields = "__all__"

class CharacterSavingThrowSerializer(serializers.ModelSerializer):
    saving_throw = SavingThrowSerializer()

    class Meta:
        model = CharacterSavingThrow
        fields = fields = ['id', 'character_id', 'saving_throw_id', 'proficient', 'saving_throw']

class CharacterSavingThrowViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all Characters' Saving Throws"""
        character_saving_throws = CharacterSavingThrow.objects.all()
        serializer = CharacterSavingThrowSerializer(character_saving_throws, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Character's Saving Throw"""
        try:
            character_saving_throw = CharacterSavingThrow.objects.get(pk=pk)
            serializer = CharacterSavingThrowSerializer(character_saving_throw, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Character.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
