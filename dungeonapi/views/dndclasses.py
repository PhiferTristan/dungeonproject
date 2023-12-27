from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from dungeonapi.models import DnDClass

class DnDClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = DnDClass
        fields = "__all__"

class DnDClassViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all Dnd Classes"""
        dnd_classes = DnDClass.objects.all()
        serializer = DnDClassSerializer(dnd_classes, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Dnd Class"""
        try:
            dnd_class = DnDClass.objects.get(pk=pk)
            serializer = DnDClassSerializer(dnd_class, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DnDClass.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
