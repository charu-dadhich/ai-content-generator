from rest_framework import serializers
from utils import (
    Responder,
    Helper,
    CustomAI
)
from app.utils.models import (
    Board,
    Standard,
    ClassWiseSubject,
    Chapter,
    ServiceType,
)
from app.prompt.models import Prompt
from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Activity
        exclude = ['created_at', 'updated_at']

    def to_representation(self, instance):
        attrs = super().to_representation(instance)
        attrs['service_type'] = instance.service_type.service_type
        return attrs


class CreateActivitySerializer(serializers.ModelSerializer):
    file_content = serializers.CharField()
    service_type_id = serializers.IntegerField()
    board_id = serializers.IntegerField()
    standard_id = serializers.IntegerField()
    subject_id = serializers.IntegerField()
    chapter_id = serializers.IntegerField()

    class Meta:
        model = Activity
        fields = ['file_content', 'service_type_id', 'board_id', 'standard_id', 'subject_id', 'chapter_id', 'generation_type', 'activity_time_in_mins', 'language', 'activity_type']

    def validate(self, attrs):
        if not (_ := ServiceType.objects.get_by_pk(attrs.get('service_type_id'))):
            Responder.accept(168)
        if attrs.get('generation_type') == 'custom' and not attrs.get('activity_time_in_mins'):
            Responder.accept(184)
        if (activity_time := attrs.get('activity_time_in_mins')) and activity_time < 5 and activity_time > 60:
            Responder.accept(185)
        if not (_ := Board.objects.get_by_pk(attrs.get('board_id'))):
            Responder.accept(155)
        if not (_ := Standard.objects.get_by_pk(attrs.get('standard_id'))):
            Responder.accept(152)
        if not (subject_obj := ClassWiseSubject.objects.get_by_pk(attrs.get('subject_id'))):
            Responder.accept(153)
        if not (chapter_obj := Chapter.objects.get_by_pk(attrs.get('chapter_id'))):
            Responder.accept(164)
        if attrs.get('file_content'):
            attrs['file_content'] = Helper.decode_file_content(attrs['file_content'])
        attrs['subject_name'] = subject_obj.subject.name
        attrs['chapter_name'] = chapter_obj.title
        return attrs

    def create(self, attrs):
        user = self.context.get('user')
        ai = CustomAI()
        activity_attrs = {
            'board_id': attrs.get('board_id'),
            'standard_id': attrs.get('standard_id'),
            'subject_id': attrs.get('subject_id'),
            'chapter_id': attrs.get('chapter_id'),
            'language': attrs.get('language', 'English'),
            'activity_time_in_mins': attrs.get('activity_time_in_mins', 20),
            'generation_type': attrs.get('generation_type'),
            'sub_subject_name': attrs.get('sub_subject_name'),
            'activity_type': attrs.get('activity_type'),
            'user': user,
            'service_type_id': attrs.get('service_type_id')
        }
        user_prompt = 'Generate an activity from this document'
        if ans := ai.generate_questions(user_prompt, attrs, activity_attrs):
            activity_attrs['description'] = ans
            activity = Activity.objects.create(**activity_attrs)
            return activity
        Responder.accept(170)
        

class ChangeActivitySerializer(serializers.Serializer):
    file_content = serializers.CharField()
    instruction = serializers.CharField()

    def validate(self, attrs):
        instance = self.instance
        if attrs.get('file_content'):
            attrs['file_content'] = Helper.decode_file_content(attrs['file_content'])
        prompt = Prompt.objects.get_by_service_type_id(instance.service_type_id)
        prompt_params = {
            'class_name': instance.standard_id,
            'subject_name': instance.subject.subject.name,
            'chapter_name': instance.chapter.title,
            'activity_time_in_mins': instance.activity_time_in_mins,
            'sub_subject_name': instance.sub_subject_name,
            'retrieved_text': attrs['file_content']
        }
        attrs['final_prompt'] = prompt.description.format(**prompt_params) + f"\n You need to change in this content: {instance.description} the following: {attrs.get('instruction')}"
        return attrs
    
    def update(self, instance, attrs):
        ai = CustomAI()
        answer = ai.chat_api(attrs.pop('final_prompt'))
        if not answer:
            Responder.accept(170)
        instance.description = answer
        instance.save()
        return instance
