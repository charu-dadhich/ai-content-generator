from django.db import models
from django.db.models import Q
from app.base.models import BaseModel
from utils import Choice


class QuestionPaperManager(models.Manager):
    def get_by_pk(self, pk):
        return self.filter(pk=pk).first()
    
    def get_last_generated_by_user(self, user):
        return self.last()

    def get_last_regenerated_by_user(self, user):
        question_paper = self.get_last_generated_by_user(user)
        question_answer = question_paper.answer_question_paper.filter(is_regenerated=True).order_by('-created_at')
        return question_answer
            

class QuestionPaper(BaseModel):
    total_marks = models.IntegerField(default=60)
    total_questions = models.IntegerField(default=5)
    standard = models.ForeignKey('utils.Standard', on_delete=models.CASCADE)
    language = models.CharField(max_length=50)
    subject = models.ForeignKey('utils.Subject', on_delete=models.CASCADE)
    paper_type = models.CharField(max_length=20, choices=Choice.PAPER_TYPE, default='hybrid')
    board = models.ForeignKey('utils.Board', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True, default=1)
    learning_objective = models.TextField(null=True, blank=True)
    chapter = models.ForeignKey('utils.Chapter', on_delete=models.CASCADE, null=True)
    topic = models.JSONField(null=True, blank=True)
    sub_topic = models.JSONField(null=True, blank=True)
    blooms_taxonomy = models.JSONField(null=True)
    is_generated_correct = models.BooleanField(default=True)
    easy_percentage = models.IntegerField(default=25)
    medium_percentage = models.IntegerField(default=50)
    difficult_percentage = models.IntegerField(default=20)
    very_challenging_percentage = models.IntegerField(default=5)
    generation_type = models.CharField(max_length=10, choices=Choice.GENERATION_TYPE, default='auto')
    service_type = models.ForeignKey('utils.ServiceType', on_delete=models.CASCADE, default=20)

    objects = QuestionPaperManager()

    class Meta:
        db_table = 'question_papers'


class DetailQuestionPaperSchemeManager(models.Manager):
    pass


class DetailQuestionPaperScheme(BaseModel):
    total_one_mark_questions = models.IntegerField()
    total_two_mark_questions = models.IntegerField()
    total_four_mark_questions = models.IntegerField()
    one_mark_answer_word_count = models.IntegerField()
    two_mark_answer_word_count = models.IntegerField()
    four_mark_answer_word_count = models.IntegerField()
    question_paper = models.ForeignKey('QuestionPaper', on_delete=models.CASCADE, null=True)

    objects = DetailQuestionPaperSchemeManager()

    class Meta:
        db_table = 'question_paper_detail'


class QuestionAnswerManager(models.Manager):
    def get_by_question_paper_id(self, question_paper_id):
        return self.filter(question_paper_id=question_paper_id, parent_question=None, is_cancelled=False)

    def get_by_question_paper_id_and_self_id(self, question_paper_id, question_answer_id):
        return self.filter(question_paper_id=question_paper_id, id=question_answer_id).first()

    def get_by_pk(self, pk):
        return self.filter(pk=pk).first()

    def get_all_with_question_id(self, pk):
        return self.filter(Q(pk=pk) | Q(replaced_for_question_id=pk))


class QuestionAnswer(BaseModel):
    # type = models.ForeignKey("base.ServiceType", on_delete=models.CASCADE)
    detail = models.TextField()
    options = models.JSONField(null=True, blank=True)
    marks = models.IntegerField(null=True, blank=True, default=0)
    question_paper = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE, related_name='answer_question_paper')
    difficulty_level = models.CharField(max_length=20, choices=Choice.DIFFICULTY_LEVEL)
    is_cancelled = models.BooleanField(default=False)
    cancellation_reason = models.TextField(default='')
    replaced_for_question = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, related_name='replaced_question_id')
    correct_answer = models.TextField(null=True, blank=True)
    answer_explanation = models.TextField(default="")
    learning_outcome = models.TextField(default="")
    question_type = models.CharField(max_length=50, default='Miscellaneous', choices=Choice.QUESTION_TYPE)
    bloom_level = models.CharField(max_length=250, default='Understand')
    skill_tag = models.CharField(max_length=50, null=True, blank=True)
    learning_competency = models.CharField(max_length=255, null=True, blank=True)
    language_competency = models.CharField(max_length=255, null=True, blank=True)
    parent_question = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='sub_question_parent_id')
    is_regenerated = models.BooleanField(default=False)

    objects = QuestionAnswerManager()

    class Meta:
        db_table = 'question_answer'


class CustomQuestionTypeDetailManager(models.Manager):
    def get_all(self):
        return self.all()


class CustomQuestionTypeDetail(BaseModel):
    question_type = models.TextField()

    objects = CustomQuestionTypeDetailManager()

    class Meta:
        db_table = 'custom_question_type_detail'


class ServiceQuestionManager(models.Manager):
    pass


class ServiceQuestion(BaseModel):
    service = models.ForeignKey('utils.ServiceType', on_delete=models.CASCADE, related_name='service_type_per_question')
    question_type = models.ForeignKey('CustomQuestionTypeDetail', on_delete=models.CASCADE, related_name='question_service_type')
    base_subject = models.ForeignKey('utils.Subject', on_delete=models.CASCADE, related_name='service_type_subject', null=True)
    grade_start = models.ForeignKey('utils.Standard', on_delete=models.CASCADE, related_name='service_question_grade_start', null=True)
    grade_end = models.ForeignKey('utils.Standard', on_delete=models.CASCADE, related_name='service_question_grade_end', null=True)

    objects = ServiceQuestionManager()

    class Meta:
        db_table = 'service_question'


# class SubQuestionManager(models.Manager):
#     pass


# class SubQuestion(BaseModel):
#     parent_question = models.ForeignKey("QuestionAnswer", on_delete=models.CASCADE, related_name="sub_questions")
#     detail = models.TextField()
#     options = models.JSONField(null=True, blank=True)
#     correct_answer = models.CharField(max_length=255, null=True, blank=True)
#     answer_explanation = models.TextField(null=True, blank=True)
#     marks = models.IntegerField()
#     bloom_level = models.CharField(max_length=250, default='Understand', choices=Choice.BLOOM_LEVEL)
#     difficulty_level = models.CharField(max_length=20, choices=Choice.DIFFICULTY_LEVEL)
    

#     objects = SubQuestionManager()

#     class Meta:
#         db_table = 'sub_questions'
