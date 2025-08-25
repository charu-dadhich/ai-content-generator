from rest_framework import serializers
from .models import LearningObjective


class CreateLearningObjectiveSerializer(serializers.ModelSerializer):
    board = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    subject = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    chapter = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title'
    )
    # blooms_taxonomy = serializers.SerializerMethodField()

    class Meta:
        model = LearningObjective
        exclude = ['created_at', 'updated_at']


    # def to_representation(self, instance):
    #     attrs = super().to_representation(instance)
    #     attrs = {
    #         'id': instance.id
    #     }
    #     return attrs