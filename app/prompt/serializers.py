from rest_framework import serializers
from .models import Prompt, SubjectSpecificPrompt, GradeSpecificPrompt


class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = '__all__'


class SubjectPromptSerializer(serializers.ModelSerializer):
    class Meta:
        model =  SubjectSpecificPrompt
        fields = '__all__'


class GradePromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeSpecificPrompt
        fields = '__all__'
