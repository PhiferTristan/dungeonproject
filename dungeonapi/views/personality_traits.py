from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from dungeonapi.models import PersonalityTrait

class PersonalityTraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalityTrait
        fields = "__all__"

class PersonalityTraitViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all Personality Traits"""
        personality_traits = PersonalityTrait.objects.all()
        serializer = PersonalityTraitSerializer(personality_traits, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Personality Trait"""
        try:
            personality_trait = PersonalityTrait.objects.get(pk=pk)
            serializer = PersonalityTraitSerializer(personality_trait, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PersonalityTrait.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
