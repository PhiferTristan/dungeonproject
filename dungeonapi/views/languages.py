from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from dungeonapi.models import Language

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"

class LanguageViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all backgrounds"""
        languages = Language.objects.all()
        serializer = LanguageSerializer(languages, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single background"""
        try:
            background = Language.objects.get(pk=pk)
            serializer = LanguageSerializer(background, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Language.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
 