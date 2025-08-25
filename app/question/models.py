
from django.db import models
from app.base.models import BaseModel
from utils import Choice


class QuestionPaperManager(models.Manager):
    def get_by_pk(self, pk):
        return self.filter(pk=pk).first()


class QuestionPaper(BaseModel):
    total_marks = models.IntegerField(default=60)
    total_questions = models.IntegerField(default=5)
    standard = models.ForeignKey('base.Standard', on_delete=models.CASCADE)
    language = models.CharField(max_length=50)
    subject = models.ForeignKey('base.Subject', on_delete=models.CASCADE)
    paper_type = models.CharField(max_length=20, choices=Choice.PAPER_TYPE, default='hybrid')
    board = models.ForeignKey('base.Board', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True, default=1)
    learning_objective = models.TextField(null=True, blank=True)
    chapter = models.ForeignKey('base.Chapter', on_delete=models.CASCADE, null=True)
    topic = models.JSONField(null=True, blank=True)
    sub_topic = models.JSONField(null=True, blank=True)
    blooms_taxonomy = models.JSONField(null=True)
    is_generated_correct = models.BooleanField(default=True)
    easy_percentage = models.IntegerField(default=25)
    medium_percentage = models.IntegerField(default=50)
    difficult_percentage = models.IntegerField(default=20)
    very_challenging_percentage = models.IntegerField(default=5)
    generation_type = models.CharField(max_length=10, choices=Choice.GENERATION_TYPE, default='auto')
    service_type = models.ForeignKey('base.ServiceType', on_delete=models.CASCADE, default=20)

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
        return self.filter(question_paper_id=question_paper_id, parent_question=None)


class QuestionAnswer(BaseModel):
    # type = models.ForeignKey("base.ServiceType", on_delete=models.CASCADE)
    detail = models.TextField()
    options = models.JSONField(null=True, blank=True)
    marks = models.IntegerField()
    question_paper = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE)
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
    parent_question = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='sub_question_parent_id')

    objects = QuestionAnswerManager()

    class Meta:
        db_table = 'question_answer'


class CustomQuestionTypeDetailManager(models.Manager):
    def get_all(self):
        return self.all()


class CustomQuestionTypeDetail(BaseModel):
    type = models.TextField()

    objects = CustomQuestionTypeDetailManager()

    class Meta:
        db_table = 'custom_question_type_detail'


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
