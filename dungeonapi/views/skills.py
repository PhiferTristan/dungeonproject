from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from dungeonapi.models import Skill, Ability

class AbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ability
        fields = ['id', 'label']

class SkillSerializer(serializers.ModelSerializer):
    ability = AbilitySerializer(read_only=True)
    class Meta:
        model = Skill
        fields = "__all__"

class SkillViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all Skills"""
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Skill"""
        try:
            skill = Skill.objects.get(pk=pk)
            serializer = SkillSerializer(skill, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Skill.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
 