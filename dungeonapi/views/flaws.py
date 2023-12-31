from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from dungeonapi.models import Flaw

class FlawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flaw
        fields = "__all__"

class FlawViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all Flaws or filtered by background_id"""
        background_id = request.query_params.get('background_id', None)

        if background_id:
            flaws = Flaw.objects.filter(background_id=background_id)
        else:
            flaws = Flaw.objects.all()

        serializer = FlawSerializer(flaws, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Flaw"""
        try:
            flaw = Flaw.objects.get(pk=pk)
            serializer = FlawSerializer(flaw, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Flaw.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
