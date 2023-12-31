from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from dungeonapi.models import Bond

class BondSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bond
        fields = "__all__"

class BondViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all Bonds or filtered by background_id"""
        background_id = request.query_params.get('background_id', None)

        if background_id:
            bonds = Bond.objects.filter(background_id=background_id)
        else:
            bonds = Bond.objects.all()

        serializer = BondSerializer(bonds, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Bond"""
        try:
            bond = Bond.objects.get(pk=pk)
            serializer = BondSerializer(bond, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Bond.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
