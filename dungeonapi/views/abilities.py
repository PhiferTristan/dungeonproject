from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from dungeonapi.models import Ability

class AbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ability
        fields = "__all__"

class AbilityViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all abilities"""
        abilities = Ability.objects.all()
        serializer = AbilitySerializer(abilities, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single ability"""
        try:
            ability = Ability.objects.get(pk=pk)
            serializer = AbilitySerializer(ability, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ability.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
