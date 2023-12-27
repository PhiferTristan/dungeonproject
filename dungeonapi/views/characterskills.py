from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from dungeonapi.models import Character, Skill, CharacterSkill

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"

class CharacterSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer()

    class Meta:
        model = CharacterSkill
        fields = fields = ['id', 'character_id', 'skill_id', 'proficient', 'skill']

class CharacterSkillViewSet(viewsets.ViewSet):
    def list(self, request):
        """Handle GET requests for all Character's Skills"""
        characterskills = CharacterSkill.objects.all()
        serializer = CharacterSkillSerializer(characterskills, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Character's Skill"""
        try:
            characterskill = CharacterSkill.objects.get(pk=pk)
            serializer = CharacterSkillSerializer(characterskill, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Character.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
