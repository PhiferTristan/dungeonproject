from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from dungeonapi.models import Ideal

class IdealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ideal
        fields = "__all__"

class IdealViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all Ideals"""
        ideals = Ideal.objects.all()
        serializer = IdealSerializer(ideals, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Ideal"""
        try:
            ideal = Ideal.objects.get(pk=pk)
            serializer = IdealSerializer(ideal, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ideal.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
