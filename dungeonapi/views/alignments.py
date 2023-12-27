from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from dungeonapi.models import Alignment

class AlignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alignment
        fields = "__all__"

class AlignmentViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all Alignments"""
        alignments = Alignment.objects.all()
        serializer = AlignmentSerializer(alignments, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Alignment"""
        try:
            alignment = Alignment.objects.get(pk=pk)
            serializer = AlignmentSerializer(alignment, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Alignment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        