from rest_framework import serializers
from app.prompt.models import Prompt
from utils import (
    Responder,
    Helper,
    CustomAI,
)
from app.utils.models import (
    Board,
    ClassWiseSubject,
    Standard,
    Chapter,
    ServiceType
)
from .models import LearningObjective


class LearningObjectiveSerializer(serializers.ModelSerializer):
    board = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    subject = serializers.SlugRelatedField(
        read_only=True,
        slug_field='subject.name'
    )
    chapter = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title'
    )
    blooms_taxonomy = serializers.SerializerMethodField()

    class Meta:
        model = LearningObjective
        exclude = ['created_at', 'updated_at']

    def get_blooms_taxonomy(self, obj):
        # if blooms_taxonomy_list := obj.blooms_taxonomy:
        #     blooms_level = [BloomsLevel.objects.get_by_pk_list(blooms_taxonomy_list)]
        #     return (blooms_level)
        return []


class GenerateLearningSerializer(serializers.ModelSerializer):
    file_content = serializers.CharField()
    service_type_id = serializers.IntegerField()
    board_id = serializers.IntegerField()
    standard_id = serializers.IntegerField()
    subject_id = serializers.IntegerField()
    chapter_id = serializers.IntegerField()
    # language = serializers.CharField()
    
    class Meta:
        model = LearningObjective
        fields = ['service_type_id', 'file_content', 'language', 'number_of_lo', 'board_id', 'standard_id', 'subject_id', 'chapter_id', 'generation_type']

    def validate(self, attrs):
        if not (service_type := ServiceType.objects.get_by_pk(attrs.get('service_type_id'))):
            Responder.accept(168)
        if service_type.service_type != 'Learning Objectives':
            Responder.accept(169)
        if attrs.get('file_content'):
            attrs['retrieved_text'] = Helper.decode_file_content(attrs['file_content'])
        if attrs.get('generation_type') == 'custom' and not attrs.get('number_of_lo'):
            Responder.accept(172)
        if (lo := attrs.get('number_of_lo')) and lo > 10 and lo < 1:
            Responder.accept(173)
        if not (_ := Board.objects.get_by_pk(attrs.get('board_id'))):
            Responder.accept(155)
        if not (_ := Standard.objects.get_by_pk(attrs.get('standard_id'))):
            Responder.accept(152)
        if not (subject_obj := ClassWiseSubject.objects.get_by_pk(attrs.get('subject_id'))):
            Responder.accept(153)
        if not (chapter_obj := Chapter.objects.get_by_pk(attrs.get('chapter_id'))):
            Responder.accept(164)
        attrs['subject_name'] = subject_obj.subject.name
        attrs['chapter_name'] = chapter_obj.title
        return attrs

    def create(self, attrs):
        user = self.context.get('user')
        user_prompt = '''Generate Learning objectives from this document.'''
        ai = CustomAI()
        learning_objective_attrs = {
            'board_id': attrs.get('board_id'),
            'standard_id': attrs.get('standard_id'),
            'subject_id': attrs.get('subject_id'),
            'chapter_id': attrs.get('chapter_id'),
            'language': attrs.get('language', 'English'),
            'number_of_lo': attrs.get('number_of_lo', 10),
            'generation_type': attrs.get('generation_type'),
            'user': user
        }
        if ans := ai.generate_questions(user_prompt, attrs, learning_objective_attrs):
            learning_objective_attrs['description'] = ans
            lo = LearningObjective.objects.create(**learning_objective_attrs)
            return lo


class ChangeLearningObjectiveSerializer(serializers.Serializer):
    file_content = serializers.CharField()
    instruction = serializers.CharField()

    def validate(self, attrs):
        instance = self.instance
        if attrs.get('file_content'):
            attrs['file_content'] = Helper.decode_file_content(attrs['file_content'])
        prompt = Prompt.objects.get_by_service_type_id(5)
        prompt_params = {
            'subject_name': instance.subject.subject.name,
            'class_name': instance.standard_id,
            'chapter_name': instance.chapter.title,
            'board_name': instance.board.name,
            'retrieved_text': attrs['file_content'],
            'number_of_lo': instance.number_of_lo
        }
        attrs['final_prompt'] = prompt.description.format(**prompt_params) + f"\n I only need to change in this content: {instance.description} the following {attrs.get('instruction')}."
        # attrs['lo'] = obj
        return attrs

    def update(self, instance, attrs):
        ai = CustomAI()
        answer = ai.chat_api(attrs.pop('final_prompt'))
        if not answer:
            Responder.accept(170)
        instance.description = answer
        instance.save()
        return instance
