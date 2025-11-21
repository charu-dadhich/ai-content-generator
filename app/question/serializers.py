from rest_framework import serializers
from django.db import transaction
from app.prompt.models import Prompt, PromptDetail
from utils.helper import Helper
from .models import QuestionAnswer, CustomQuestionTypeDetail, QuestionPaper
from app.utils.models import (
    Board,
    Standard,
    Chapter,
    ClassWiseSubject,
)
from utils import (
    Responder,
    CustomAI,
    Validator,
)


class QuestionAnswerSerializer(serializers.ModelSerializer):
    blooms_taxonomy = serializers.SerializerMethodField()
    sub_questions = serializers.SerializerMethodField()

    class Meta:
        model = QuestionAnswer
        fields = ('id', 'question_type', 'detail', 'options', 'marks', 'question_paper', 'difficulty_level', 'correct_answer', 'answer_explanation', 'learning_outcome', 'blooms_taxonomy', 'sub_questions', 'skill_tag') 

    def get_blooms_taxonomy(self, obj):
        return obj.bloom_level
    
    def get_sub_questions(self, obj):
        if obj.parent_question is None:
            sub_qs = obj.sub_question_parent_id.all()
            return QuestionAnswerSerializer(sub_qs, many=True, context={**self.context, "exclude_sub_questions": True}).data
        return None

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if self.context.get("exclude_sub_questions"):
            rep.pop("sub_questions", None)
        return rep


class CustomQuestionTypeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomQuestionTypeDetail
        fields = ['id', 'question_type']


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
    service_type = serializers.SerializerMethodField()

    class Meta:
        model = QuestionPaper
        fields = ['id', 'board', 'standard', 'chapter', 'blooms_taxonomy', 'paper_type', 'total_questions', 'subject', 'service_type']
    
    def get_service_type(self, obj):
        return obj.service_type.service_type


class QuestionDetailSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    instruction = serializers.CharField()
    # old_content = serializers.CharField()


class QuestionTypeDetailSerializer(serializers.Serializer):
    marks_per_question = serializers.IntegerField()
    number_of_questions = serializers.IntegerField()
    total_sub_questions = serializers.IntegerField(required=False)
    sub_subjective_questions = serializers.IntegerField(required=False)
    sub_objective_questions = serializers.IntegerField(required=False)
    word_limit = serializers.IntegerField(required=False)
    marks_per_objective_question = serializers.IntegerField(required=False)
    marks_per_subjective_question = serializers.IntegerField(required=False)


class GeneratedQuestionSerializer(serializers.Serializer):
    board_id = serializers.IntegerField()
    standard_id = serializers.IntegerField()
    subject_id = serializers.IntegerField()
    chapter_id = serializers.IntegerField()
    language = serializers.CharField(required=False)
    service_type_id = serializers.IntegerField()
    topic = serializers.CharField(required=False)
    sub_topic = serializers.CharField(required=False)
    objective = serializers.CharField(required=False)
    generation_type = serializers.CharField()
    file_content = serializers.CharField()
    mcqs = serializers.ListField(child=QuestionTypeDetailSerializer(), required=False)
    assertion_reason = serializers.ListField(child=QuestionTypeDetailSerializer(), required=False)
    case_based = serializers.ListField(child=QuestionTypeDetailSerializer(), required=False)
    paragraph_based = serializers.ListField(child=QuestionTypeDetailSerializer(), required=False)
    fill_in_the_blanks = serializers.ListField(child=QuestionTypeDetailSerializer(), required=False)
    match_the_following = serializers.ListField(child=QuestionTypeDetailSerializer(), required=False)
    short_answer = serializers.ListField(child=QuestionTypeDetailSerializer(), required=False)
    long_answer = serializers.ListField(child=QuestionTypeDetailSerializer(), required=False)
    application_based = serializers.ListField(child=QuestionTypeDetailSerializer(), required=False)
    reference_to_context = serializers.ListField(child=QuestionTypeDetailSerializer(), required=False)
    statement_based = serializers.ListField(child=QuestionTypeDetailSerializer(), required=False)
    parallel = serializers.ListField(child=QuestionTypeDetailSerializer(), required=False)
    writing_skill = serializers.ListField(child=QuestionTypeDetailSerializer(), required=False)
    source_based = serializers.ListField(child=QuestionTypeDetailSerializer(), required=False)
    critical_analysis = serializers.ListField(child=QuestionTypeDetailSerializer(), required=False)
    if_based = serializers.ListField(child=QuestionTypeDetailSerializer(), required=False)
    easy_percentage = serializers.IntegerField(required=False)
    medium_percentage = serializers.IntegerField(required=False)
    difficult_percentage = serializers.IntegerField(required=False)
    very_challenging_percentage = serializers.IntegerField(required=False)
    total_questions = serializers.IntegerField(min_value=1, max_value=15, required=False)
    bloom_filters = serializers.ListField(required=False)  

    def validate(self, attrs):
        board_id = attrs.get('board_id')
        standard_id = attrs.get('standard_id')
        subject_id = attrs.get('subject_id')
        chapter_id = attrs.get('chapter_id')
        file_data = attrs.get('file_content')
        generation_type = attrs.get('generation_type')
        if not (_ := Board.objects.get_by_pk(board_id)):
            Responder.accept(155)
        if not (_ := Standard.objects.get_by_pk(standard_id)):
            Responder.accept(152)
        if not (subject_obj := ClassWiseSubject.objects.get_by_pk(subject_id)):
            Responder.accept(153)
        if not (chapter_obj := Chapter.objects.get_by_pk(chapter_id)):
            Responder.accept(154)
        if file_data:
            attrs['retrieved_text'] = Helper.decode_file_content(file_data)
        self._validate_required_fields(generation_type)
        attrs['subject_name'] = subject_obj.subject.name
        attrs['chapter_name'] = chapter_obj.title
        attrs['subject_id'] = subject_obj.subject_id
        return attrs

    def _validate_required_fields(self, generation_type):
        if generation_type == "custom":
            custom_question_configuration = ['if_based', 'critical_analysis', 'source_based', 'short_answer', 'writing_skill', 'parallel', 'statement_based', 'reference_to_context', 'application_based', 'long_answer', 'long_answer', 'match_the_following', 'fill_in_the_blanks', 'paragraph_based', 'case_based', 'assertion_reason', 'mcqs']
            difficulty_level_metrics = ['easy_percentage', 'medium_percentage', 'difficult_percentage', 'very_challenging_percentage']
            if not (any(custom_question_configuration) and any(difficulty_level_metrics)):
                Responder.accept(165)
            return

    def create(self, attrs):
        question_paper_attrs = {
            'standard_id': attrs.get('standard_id'),
            'board_id': attrs.get('board_id'),
            'subject_id': attrs.get('subject_id'),
            'chapter_id': attrs.get('chapter_id'),
            'language': attrs.get('language', 'English'),
            'topic': attrs.get('topic'),
            'sub_topic': attrs.get('sub_topic'),
            'generation_type': attrs.get('generation_type'),
            'total_questions': attrs.get('total_questions', 15),
            'blooms_taxonomy': attrs.get('bloom_filters', []),
            'service_type_id': attrs.get('service_type_id')
        }
        ai = CustomAI()
        user_prompt = f'''Generate questions based on class {question_paper_attrs.get('standard_id')} cbse subject {attrs.get('subject_name')} and chapter {attrs.get('chapter_name')}'''
        if ans := ai.generate_questions(user_prompt, attrs, question_paper_attrs):
            if response := Validator.extract_json_from_ai_response(ans):
                with transaction.atomic():
                    question_paper = QuestionPaper.objects.create(**question_paper_attrs)
                    answers = self._create_question_answer(response, question_paper)
                return question_paper, answers
        Responder.accept(167)

    def _create_question_answer(self, res, question_paper):
        questions = []
        if res:
            for r in res:
                if not r.get('sub_questions'):
                    r['detail'] = r.pop('question', '')
                    r.pop('question_number', '')
                    r.pop('answer_word_count', '')
                    r['question_type'] = r.pop('type_of_question', '')
                    r['correct_answer'] = r.pop('correct_option', '')
                    r['question_paper'] = question_paper
                    r['bloom_level'] = r.pop('blooms_taxonomy', '')
                    r.pop('sub_questions', '')
                    questions.append(QuestionAnswer.objects.create(**r))
                else:
                    r.pop('question_number', '')
                    r.pop('answer_word_count', '')
                    x = {
                        'detail': r.pop('question', ''),
                        'question_type': r.pop('type_of_question', ''),
                        'marks': r.pop('marks', ''),
                        'question_paper': question_paper
                    }
                    qa_id = QuestionAnswer.objects.create(**x)
                    for sq in r['sub_questions']:
                        sq['parent_question'] = qa_id
                        sq['question_paper'] = question_paper
                        sq['correct_answer'] = sq.pop('correct_option', '')
                        sq['bloom_level'] = sq.pop('blooms_taxonomy', '')
                        sq['question_type'] = x['question_type']
                        sq.pop('sub_question_number', '')
                        sq.pop('answer_word_count', '')
                        questions.append(QuestionAnswer.objects.create(**sq))
            return questions


class RegenerateQuestionSerializer(serializers.Serializer):
    question_paper_id = serializers.IntegerField()
    regeneration_data = QuestionDetailSerializer(many=True)
    file_content = serializers.CharField()

    def validate(self, attrs):
        regeneration_data = attrs.get('regeneration_data', [])
        if not (question_paper := QuestionPaper.objects.get_by_pk(attrs.get('question_paper_id'))):
            return Responder.accept(159)
        if not attrs.get('regeneration_data'):
            return Responder.accept(163)
        if not (prompt := Prompt.objects.get_by_service_type_id(question_paper.service_type)):
            return Responder.accept(161)
        if attrs.get('file_content'):
            content = Helper.decode_file_content(attrs['file_content'])  

        add_on_prompt = ''
        for i in regeneration_data:
            if not (question_answer := QuestionAnswer.objects.get_by_question_paper_id_and_self_id(attrs['question_paper_id'], i['question_id'])):
                return Responder.accept(160)
            old_content = f"Question: {question_answer.detail} correct_answer: {question_answer.correct_answer} answer_explanation: {question_answer.answer_explanation} learning_outcome: {question_answer.learning_outcome}"
            add_on_prompt += f"For question_id {i['question_id']} having content as follows:, {old_content}, replace it with the following: {i['instruction']}\n"
        total_questions = len(regeneration_data)
        final_params = {
            'total_questions': total_questions,
            'class_name': question_paper.standard_id,
            'subject_name': question_paper.subject.name,
            'board_name': question_paper.board.name,
            'chapter_name': question_paper.chapter.title,
            'question_type_block': add_on_prompt,
            'easy_percentage': 0,
            'medium_percentage': 0,
            'very_challenging_percentage': 100,
            'difficult_percentage': 0,
            'topic': '',
            'sub_topic': '',
            'retrieved_text': content
        }
        final_prompt = prompt.description.format(
            **final_params
        )
        if prompt_detail := PromptDetail.objects.get_by_prompt_class_subject(prompt, question_paper.standard_id, question_paper.subject_id):
            final_prompt = final_prompt.replace("__SUBJECT_SPECIFIC_GUIDELINES__", prompt_detail.description)
        final_prompt += f"\n Make sure that each question contains a field called `replaced_for_question_id`, and this field should be an integer that corresponds to the old question ID that the new question is replacing. The field should **not** be a list of IDs, just a single integer. The question type should be {question_answer.question_type} and should be of marks {question_answer.marks} only."
        attrs['final_params'] = final_params
        attrs['question_answer'] = question_answer
        ai = CustomAI()
        ans = ai.chat_api(final_prompt)
        response = Validator.extract_json_from_ai_response(ans)
        attrs['response'] = response
        attrs['question_paper'] = question_paper
        return attrs

    def create(self, attrs):
        question_answer = attrs.pop('question_answer')
        response = attrs.pop('response')
        question_answer.is_cancelled = True
        question_answer.cancellation_reason = "Not appropriate"
        question_paper = attrs.pop('question_paper')
        for r in response: 
            if not r.get('sub_questions'):
                r['detail'] = r.pop('question', '')
                r.pop('question_number', '')
                r.pop('answer_word_count', '')
                r['question_type'] = r.pop('type_of_question')
                r['correct_answer'] = r.pop('correct_option', '')
                r['question_paper_id'] = attrs.get('question_paper_id')
                r['bloom_level'] = r.pop('blooms_taxonomy', '')
                r.pop('word_limit', '')
                r.pop('sub_questions', '')
                QuestionAnswer.objects.create(**r)
                old_question = QuestionAnswer.objects.get_by_pk(r.get('replaced_for_question_id'))
                old_question.is_cancelled=True
                old_question.save()
            else:
                new_questions = []
                r.pop('question_number', '')
                r.pop('answer_word_count', '')
                x = {
                    'detail': r.pop('question', ''),
                    'question_type': r.pop('type_of_question', ''),
                    'marks': r.pop('marks', ''),
                    'question_paper_id': attrs.get('question_paper_id')
                }
                qa_id = QuestionAnswer.objects.create(**x)
                new_questions.append(qa_id)
                for sq in r['sub_questions']:
                    sq['parent_question'] = qa_id
                    sq['question_paper_id'] = attrs.get('question_paper_id')
                    sq['correct_answer'] = sq.pop('correct_option', '')
                    sq['bloom_level'] = sq.pop('blooms_taxonomy', '')
                    sq['question_type'] = x['question_type']
                    sq.pop('sub_question_number', '')
                    sq.pop('answer_word_count', '')
                    new_questions.append(QuestionAnswer.objects.create(**sq))
                    old_question = QuestionAnswer.objects.get_by_pk(r.get('replaced_for_question_id'))
                    old_question.is_cancelled=True
                    old_question.save()
        return {'question_paper': question_paper}
