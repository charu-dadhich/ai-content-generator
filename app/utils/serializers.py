from rest_framework import serializers
from .models import (
    Chapter,
    Board,
    Standard,
    Subject,
    ServiceType,
    BloomsLevel,
    LLMModel,
    ClassWiseSubject,
)


class AllChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ["name", "id"]


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["name", "id"]


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Standard
        fields = ["id", "name"]


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "name"]


class ClassWiseSubjectSerializer(serializers.ModelSerializer):
    name = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), source='subject.name')

    class Meta:
        model = ClassWiseSubject
        fields = ["id", "name"]


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ["id", "title"]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ["id", "service_type"]


class BloomLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloomsLevel
        fields = ["id", "name", "icon"]


class LLMDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLMModel
        fields = "__all__"
