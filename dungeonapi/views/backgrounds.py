from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from dungeonapi.models import Background

class BackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Background
        fields = "__all__"

class BackgroundViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all backgrounds"""
        backgrounds = Background.objects.all()
        serializer = BackgroundSerializer(backgrounds, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single background"""
        try:
            background = Background.objects.get(pk=pk)
            serializer = BackgroundSerializer(background, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Background.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
       