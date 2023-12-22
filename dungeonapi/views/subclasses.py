from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from dungeonapi.models import Subclass

class SubclassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subclass
        fields = "__all__"

class SubclassViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all subclasses"""
        subclasses = Subclass.objects.all()
        serializer = SubclassSerializer(subclasses, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single subclass"""
        try:
            subclass = Subclass.objects.get(pk=pk)
            serializer = SubclassSerializer(subclass, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Subclass.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
 