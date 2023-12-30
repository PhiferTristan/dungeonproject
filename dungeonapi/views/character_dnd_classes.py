from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from dungeonapi.models import Character, DnDClass, CharacterDnDClass

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = "__all__"

class DnDClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = DnDClass
        fields = "__all__"

class CharacterDnDClassSerializer(serializers.ModelSerializer):
    character = CharacterSerializer()
    dnd_class = DnDClassSerializer()

    class Meta:
        model = CharacterDnDClass
        fields = fields = ['id', 'character', 'dnd_class']

class CharacterDnDClassViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all Characters' Classes"""
        character_dnd_classes = CharacterDnDClass.objects.all()
        serializer = CharacterDnDClassSerializer(character_dnd_classes, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Character's Class"""
        try:
            character_dnd_class = CharacterDnDClass.objects.get(pk=pk)
            serializer = CharacterDnDClassSerializer(character_dnd_class, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CharacterDnDClass.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
