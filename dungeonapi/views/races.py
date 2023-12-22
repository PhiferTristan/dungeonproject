from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from dungeonapi.models import Race

class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = ['id', 'label', 'description']

class RaceViewSet(viewsets.ViewSet):
    """Handle GET requests for all races
    
    Returns:
        Response -- Multiple JSON serialized objects
    """
    def list (self, request):
        races = Race.objects.all()
        serializer = RaceSerializer(races, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single race
        
        Returns:
            Response -- JSON serialized object
        """
        try:
            race = Race.objects.get(pk=pk)
            serializer = RaceSerializer(race, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Race.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        