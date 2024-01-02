from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from dungeonapi.models import Background, Skill

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'label']

class BackgroundSerializer(serializers.ModelSerializer):
    skill_prof_1 = SkillSerializer(read_only=True)
    skill_prof_2 = SkillSerializer(read_only=True)
    class Meta:
        model = Background
        fields = "__all__"

class BackgroundViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all Backgrounds"""
        backgrounds = Background.objects.all()
        serializer = BackgroundSerializer(backgrounds, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Background"""
        try:
            background = Background.objects.get(pk=pk)
            serializer = BackgroundSerializer(background, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Background.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
       