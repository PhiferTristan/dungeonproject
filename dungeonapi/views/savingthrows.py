from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from dungeonapi.models import SavingThrow

class SavingThrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingThrow
        fields = "__all__"

class SavingThrowViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all saving throws"""
        saving_throws = SavingThrow.objects.all()
        serializer = SavingThrowSerializer(saving_throws, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single saving throw"""
        try:
            saving_throw = SavingThrow.objects.get(pk=pk)
            serializer = SavingThrowSerializer(saving_throw, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SavingThrow.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
