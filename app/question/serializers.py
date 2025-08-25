from rest_framework import serializers
from .models import QuestionAnswer, CustomQuestionTypeDetail, QuestionPaper
from app.base.serializers import BloomLevelSerializer
from app.base.models import BloomsLevel


class QuestionAnswerSerializer(serializers.ModelSerializer):
    # learning_objective = serializers.SerializerMethodField()
    # type = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='type'
    # )
    blooms_taxonomy = serializers.SerializerMethodField()
    sub_questions = serializers.SerializerMethodField()

    class Meta:
        model = QuestionAnswer
        fields = ('question_type', 'detail', 'options', 'marks', 'question_paper', 'difficulty_level', 'correct_answer', 'answer_explanation', 'learning_outcome', 'blooms_taxonomy', 'sub_questions', 'skill_tag') 

    def get_blooms_taxonomy(self, obj):
        print("parent ",obj.parent_question)
        return obj.bloom_level
        # if obj.parent_question is not None:
        #     print("inside", obj.bloom_level)
        # else:
        #     return obj.bloom_level
        # return []
    
    def get_sub_questions(self, obj):
        if obj.parent_question is None:
            sub_qs = obj.sub_question_parent_id.all()
            return QuestionAnswerSerializer(sub_qs, many=True, context={**self.context, "exclude_sub_questions": True}).data
        return None

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # If we're in a nested sub-question context, remove `sub_questions`
        if self.context.get("exclude_sub_questions"):
            rep.pop("sub_questions", None)
        return rep



class CustomQuestionTypeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomQuestionTypeDetail
        fields = ['id', 'type']


class QuestionPaperSerializer(serializers.ModelSerializer):
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
    blooms_taxonomy = serializers.SerializerMethodField()

    class Meta:
        model = QuestionPaper
        fields = ['id', 'board', 'standard', 'chapter', 'blooms_taxonomy', 'paper_type', 'total_questions', 'subject']

    def get_blooms_taxonomy(self, obj):
        print("inside finding blooms taxonomy", obj)
        if blooms_taxonomy_list := obj.blooms_taxonomy:
            blooms_level = [BloomsLevel.objects.get_by_pk_list(blooms_taxonomy_list)]
            print("levels with name", blooms_level)
            return (blooms_level)
        return []
