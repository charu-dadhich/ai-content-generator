from django import forms
from .models import LearningObjective
from django.conf import settings
from django.core.exceptions import ValidationError
from app.utils.models import Board, Standard, Chapter, Subject
from utils import CustomAI, Validator
import os
import time
import random


class LearningObjectiveForm(forms.ModelForm):
    file_input = forms.FileField()
    service_type_id = forms.IntegerField()
    board_id = forms.IntegerField()
    standard_id = forms.IntegerField()
    subject_id = forms.IntegerField()
    chapter_id = forms.IntegerField()
    number_of_lo = forms.IntegerField(required=False, validators=[])

    class Meta:
        model = LearningObjective
        fields = ['file_input', 'number_of_lo', 'language', 'service_type_id', 'board_id', 'standard_id', 'subject_id', 'chapter_id', 'generation_type']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        # self.fields['number_of_lo'].validators.clear()
        # self.fields['number_of_lo'].default.clear()

    def clean(self):
        print("in clean method of lo")
        cleaned_data = super().clean()
        file_data = cleaned_data.get('file_input')
        print(cleaned_data.get('number_of_lo'), "********************")
        print(cleaned_data)
        board_id = cleaned_data.get('board_id')
        grade_id = cleaned_data.get('standard_id')
        subject_id = cleaned_data.get('subject_id')
        chapter_id = cleaned_data.get('chapter_id')
        # generation_type = cleaned_data.get('generation_type')
        if not (board_obj := Board.objects.get_by_pk(board_id)):
            raise ValidationError("not correct id is sent")
        if not (grade_obj := Standard.objects.get_by_pk(grade_id)):
            raise ValidationError("not correct id is sent")
        if not (subject_obj := Subject.objects.get_by_pk(subject_id)):
            raise ValidationError("not correct id is sent")
        if not (chapter_obj := Chapter.objects.get_by_pk(chapter_id)):
            raise ValidationError("not correct id is sent")
        if file_data:
            file_path = os.path.join(settings.MEDIA_ROOT, f'upload_docs\{file_data.name}')
            print(file_path)
            seconds_since_epoch = int(time.time())
            random_number = random.randint(10000, 99999)
            name, ext = file_data.name.split('.')
            print(name, ext)
            custom_file_path = f'media/upload_docs/{name}-{seconds_since_epoch}-{random_number}.{ext}'
            with open(custom_file_path, 'wb+') as destination:
                print("isi")
                for chunk in file_data.chunks():
                    destination.write(chunk)
            cleaned_data['custom_file_path'] = custom_file_path
        cleaned_data['subject_name'] = subject_obj.name
        cleaned_data['chapter_name'] = chapter_obj.title
        print(cleaned_data)
        return cleaned_data

    def save(self, commit=True, **kwargs):
        cleaned_data = self.cleaned_data
        print("in saving the data", cleaned_data)
        user_prompt = '''Generate Learning objectives from this document.'''
        file_path = cleaned_data.get('custom_file_path')
        print("cleaned data in create", cleaned_data)
        ai = CustomAI(file_path)
        learning_objective_attrs = {
            'board_id': cleaned_data.get('board_id'),
            'standard_id' : cleaned_data.get('standard_id'),
            'subject_id' : cleaned_data.get('subject_id'),
            'chapter_id' : cleaned_data.get('chapter_id'),
            'language': cleaned_data.get('language'),
            'number_of_lo': cleaned_data.get('number_of_lo'),
            'generation_type': cleaned_data.get('generation_type')
        }
        print("before create", cleaned_data)
        if ans := ai.generate_questions(user_prompt, cleaned_data, learning_objective_attrs):
            learning_objective_attrs['description'] = ans
            lo = LearningObjective.objects.create(**learning_objective_attrs)
            print("lo-------", lo)
            return lo
