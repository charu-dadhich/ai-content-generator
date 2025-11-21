import os
import time
import random
import demjson3
import re
from django import forms
from django.db import transaction
from django.core.exceptions import ValidationError
from django.conf import settings
from app.utils.models import Board, Standard, Chapter, Subject, ServiceType
from .models import QuestionPaper, DetailQuestionPaperScheme, QuestionAnswer
from utils.gpt import CustomAI
from utils import Validator
from django.http import JsonResponse


class GeneratedQuestionForm(forms.Form):
    board_id = forms.IntegerField()
    standard_id = forms.IntegerField()
    subject_id = forms.IntegerField()
    chapter_id = forms.IntegerField()
    language = forms.CharField(required=False)
    service_type_id = forms.IntegerField(required=False)
    topic = forms.CharField(required=False)
    sub_topic = forms.CharField(required=False)
    objective = forms.CharField(required=False)
    generation_type = forms.CharField()
    file_input = forms.FileField(required=False)
    mcqs = forms.JSONField(required=False)
    assertion_reason = forms.JSONField(required=False)
    case_based = forms.JSONField(required=False)
    paragraph_based = forms.JSONField(required=False)
    fill_in_the_blanks = forms.JSONField(required=False)
    match_the_following = forms.JSONField(required=False)
    short_answer = forms.JSONField(required=False)
    long_answer = forms.JSONField(required=False)
    application_based = forms.JSONField(required=False)
    reference_to_context = forms.JSONField(required=False)
    statement_based = forms.JSONField(required=False)
    parallel = forms.JSONField(required=False)
    writing_skill = forms.JSONField(required=False)
    source_based = forms.JSONField(required=False)
    critical_analysis = forms.JSONField(required=False)
    if_based = forms.JSONField(required=False)
    easy_percentage = forms.IntegerField(required=False)
    medium_percentage = forms.IntegerField(required=False)
    difficult_percentage = forms.IntegerField(required=False)
    very_challenging_percentage = forms.IntegerField(required=False)
    total_questions = forms.IntegerField(min_value=1, max_value=15, required=False)
    bloom_filters = forms.JSONField(required=False)

    def clean(self):
        print("i am here")
        cleaned_data = super().clean()
        print(cleaned_data)
        board_id = cleaned_data.get('board_id')
        standard_id = cleaned_data.get('standard_id')
        subject_id = cleaned_data.get('subject_id')
        chapter_id = cleaned_data.get('chapter_id')
        file_data = cleaned_data.get('file_input')
        generation_type = cleaned_data.get('generation_type')
        if not file_data:
            print("inside not foun")
            raise ValidationError("File not uploaded. Try again.")
            # return JsonResponse({'message': "FIle not uploaded. Try again", 'status_code': 400, 'status': False})
        else:
            file_path = os.path.join(settings.MEDIA_ROOT, f'upload_docs\{file_data.name}')
            print("path of file",file_path)
        if not (board_obj := Board.objects.get_by_pk(board_id)):
            raise ValidationError("not correct id is sent")
        if not (grade_obj := Standard.objects.get_by_pk(standard_id)):
            raise ValidationError("not correct id is sent")
        if not (subject_obj := Subject.objects.get_by_pk(subject_id)):
            raise ValidationError("not correct id is sent")
        if not (chapter_obj := Chapter.objects.get_by_pk(chapter_id)):
            raise ValidationError("not correct id is sent")
        print("in form",cleaned_data)
        if file_data:
            print("if", file_data)
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

        self._validate_required_fields(generation_type)

        print("clean-----", file_data)
        print("chpa",chapter_obj, chapter_obj.id, chapter_obj.title)
        cleaned_data['subject_name'] = subject_obj.name
        cleaned_data['chapter_name'] = chapter_obj.title
        return cleaned_data

    def _validate_required_fields(self, generation_type):
        if generation_type == "custom":
            custom_question_configuration = ['if_based', 'critical_analysis', 'source_based', 'short_answer', 'writing_skill', 'parallel', 'statement_based', 'reference_to_context', 'application_based', 'long_answer', 'long_answer', 'match_the_following', 'fill_in_the_blanks', 'paragraph_based', 'case_based', 'assertion_reason', 'mcqs']
            difficulty_level_metrics = ['easy_percentage', 'medium_percentage', 'difficult_percentage', 'very_challenging_percentage']
            print(self.cleaned_data.get('total_questions'))
            print(any(custom_question_configuration))
            print(any(difficulty_level_metrics))
            if any(custom_question_configuration) and any(difficulty_level_metrics):
                print("yes I am in")
            else:
                print("here is the error")
                raise ValidationError("some values are  missing")
            return

    def save(self, commit=True, **kwargs):
        # instance = super().save(commit=False)
        cleaned_data = self.cleaned_data
        print("cleaned-----------",self.cleaned_data)
        question_paper_attrs = {
            'standard_id': cleaned_data.get('standard_id'),
            'board_id': cleaned_data.get('board_id'),
            'subject_id': cleaned_data.get('subject_id'),
            'chapter_id': cleaned_data.get('chapter_id'),
            'language': cleaned_data.get('language'),
            'topic': cleaned_data.get('topic'),
            'sub_topic': cleaned_data.get('sub_topic'),
            'generation_type': cleaned_data.get('generation_type'),
            'total_questions': cleaned_data.get('total_questions') or 15,
            'blooms_taxonomy': cleaned_data.get('bloom_filters') or [],
            'service_type_id': cleaned_data.get('service_type_id')
        }
        if file_path := cleaned_data.get('custom_file_path'):
            ai = CustomAI(file_path)
        user_prompt = '''Generate Learning objectives from this document.'''
        # user_prompt = '''Generate questions based on class {question_paper_attrs.get('standard_id')} cbse subject {cleaned_data.get('subject_name')} and chapter cleaned_data.get('chapter_name')'''
        if ans := ai.generate_questions(user_prompt, cleaned_data, question_paper_attrs):
            if response := Validator.extract_json_from_ai_response(ans):
                with transaction.atomic():
                    print("question-apper-attrs", question_paper_attrs)
                    question_paper = QuestionPaper.objects.create(**question_paper_attrs)
                    # self._create_question_detail_scheme(question_paper)
                    print("response generated", response)
                    answers = self._create_question_answer(response, question_paper)
                return question_paper, answers
        return {}

    def _create_question_detail_scheme(self, question_paper):
        paper_scheme_attrs = {
            'total_one_mark_questions': settings.DEFAULT_ONE_MARK_QUESTIONS,
            'total_two_mark_questions': settings.DEFAULT_TWO_MARK_QUESTIONS,
            'total_four_mark_questions': settings.DEFAULT_FOUR_MARK_QUESTIONS,
            'one_mark_answer_word_count': 50,
            'two_mark_answer_word_count': 100,
            'four_mark_answer_word_count': 200,
            'question_paper': question_paper
        }
        paper_scheme = DetailQuestionPaperScheme.objects.create(**paper_scheme_attrs)

    def _create_question_answer(self, res, question_paper):
        questions = []
        if res:
            print("all gen ques", res)
            for r in res:
                print("r------>" ,r)
                if not r.get('sub_questions'):
                    r['detail'] = r.pop('question', '')
                    r.pop('question_number', '')
                    r.pop('answer_word_count', '')
                    
                    # type_name = r.pop('type_of_question', '')
                    # if type := ServiceType.objects.filter(service_type=type_name).first():
                    #     r['type'] = type
                    # else:
                    #     r['type_id'] = 1
                    r['question_type'] = r.pop('type_of_question')
                    r['correct_answer'] = r.pop('correct_option', '')
                    r['question_paper'] = question_paper
                    r['bloom_level'] = r.pop('blooms_taxonomy', '')
                    r.pop('sub_questions', '')
                    # skill = r.pop('skill_tag')
                    # print("skills",skill)
                    print("vale of main parent answer",r)
                    questions.append(QuestionAnswer.objects.create(**r))
                else:
                    print("else fo sq")
                    r.pop('question_number', '')
                    r.pop('answer_word_count', '')
                    x = {
                        'detail': r.pop('question', ''),
                        'question_type': r.pop('type_of_question', ''),
                        'marks': r.pop('marks', ''),
                        'question_paper': question_paper
                    }
                    print(x)
                    print(r)
                    qa_id = QuestionAnswer.objects.create(**x)
                    for sq in r['sub_questions']:
                        sq['parent_question'] = qa_id
                        sq['question_paper'] = question_paper
                        sq['correct_answer'] = sq.pop('correct_option', '')
                        sq['bloom_level'] = sq.pop('blooms_taxonomy', '')
                        sq['question_type'] = x['question_type']
                        sq.pop('sub_question_number', '')
                        sq.pop('answer_word_count', '')
                        print(sq)
                        QuestionAnswer.objects.create(**sq)
            return questions

    # def _extract_json_from_ai_response(self, ans):
    #     cleaned_text = re.sub(r"```json\s*([\s\S]*?)```", r"\1", ans, flags=re.MULTILINE)

    #     # If the above doesn't catch, also try removing any backticks wrapping whole string
    #     cleaned_text = cleaned_text.strip('` \n\r\t')

    #     # Now parse cleaned JSON string
    #     try:
    #         data = demjson3.decode(cleaned_text)
    #         return data
    #     except Exception as e:
    #         print(f"Error parsing JSON: {e}")
    #         return None