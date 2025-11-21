from django.db import models
from app.base.models import BaseModel


class SubjectManager(models.Manager):
    pass


class Subject(BaseModel):
    name = models.CharField(max_length=255)

    objects = SubjectManager()

    class Meta:
        db_table = 'subjects'

    def __str__(self):
        return self.name


class Department(BaseModel):
    name = models.CharField(max_length=60)

    class Meta:
        db_table = 'departments'

    def __str__(self):
        return self.name


class BoardManager(models.Manager):
    def get_by_pk(self, pk):
        return self.filter(pk=pk).first()


class Board(BaseModel):
    name = models.CharField(max_length=10, unique=True)

    objects = BoardManager()

    class Meta:
        db_table = 'boards'


class StandardManager(models.Manager):
    def get_by_pk(self, pk):
        return self.filter(pk=pk).first()


class Standard(BaseModel):
    name = models.CharField(max_length=10, unique=True)

    objects = StandardManager()

    class Meta:
        db_table = 'standards'


class ClassWiseSubjectManager(models.Manager):
    def get_by_standard(self, standard):
        return self.filter(standard=standard)

    def get_by_pk(self, pk):
        return self.filter(pk=pk).first()


class ClassWiseSubject(BaseModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, default=0) # remove this in final migration

    objects = ClassWiseSubjectManager()

    class Meta:
        db_table = 'class_wise_subjects'


class ChapterManager(models.Manager):
    def get_by_subject_and_board(self, subject, board):
        return self.filter(subject=subject, board=board)

    def get_by_pk(self, pk):
        return self.filter(pk=pk).first()


class Chapter(BaseModel):
    subject = models.ForeignKey('ClassWiseSubject', on_delete=models.CASCADE)
    title = models.CharField(max_length=500, unique=True)
    board = models.ForeignKey('Board', on_delete=models.CASCADE, default=1)

    objects = ChapterManager()

    class Meta:
        db_table = 'chapters'


class ServiceTypeManager(models.Manager):
    def get_by_pk(self, pk):
        return self.filter(pk=pk).first()


class ServiceType(BaseModel):
    service_type = models.CharField(max_length=255)

    objects = ServiceTypeManager()

    class Meta:
        db_table = 'service_types'

    def __str__(self):
        return self.service_type


class ServiceGradeManager(models.Manager):
    def get_by_grade(self, grade_id):
        return self.filter(grade_start_id__lte=grade_id, grade_end_id__gte=grade_id).select_related('service_type').order_by('service_type__id')


class ServiceGrade(BaseModel):
    grade_start = models.ForeignKey('Standard', on_delete=models.CASCADE, related_name='service_class_start')
    grade_end = models.ForeignKey('Standard', on_delete=models.CASCADE, related_name='service_class_end')
    service_type = models.OneToOneField('ServiceType', on_delete=models.CASCADE, related_name='service_per_class')

    objects = ServiceGradeManager()

    class Meta:
        db_table = 'service_grade'


class BloomsLevelManager(models.Manager):
    def get_by_pk_list(self, pk_list):
        return list(self.filter(pk__in=pk_list).values_list('name', flat=True))


class BloomsLevel(BaseModel):
    name = models.CharField(max_length=50)
    icon = models.TextField(default='')

    objects = BloomsLevelManager()

    class Meta:
        db_table = 'blooms_level'


class LLMModelManager(models.Manager):
    def get_by_pk(self, pk):
        return self.filter(pk=pk).first()
    

class LLMModel(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    model = models.CharField(max_length=70)

    objects = LLMModelManager()

    class Meta:
        db_table = 'llm_model'
