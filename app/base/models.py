from django.db import models
from utils import Choice


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def update(self, **attrs):
        for key, value in attrs:
            self.update(key=value)
        return


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


class SubjectManager(models.Manager):
    def get_by_standard(self, standard):
        return self.filter(standard=standard)
    
    def get_by_pk(self, pk):
        return self.filter(pk=pk).first()


class Subject(BaseModel):
    name = models.CharField(max_length=100)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, default=0) # remove this in final migration

    objects = SubjectManager()

    class Meta:
        db_table = 'subjects'
        unique_together = (('name', 'standard'),)


class ChapterManager(models.Manager):
    def get_by_subject(self, subject):
        return self.filter(subject=subject)

    def get_by_pk(self, pk):
        return self.filter(pk=pk).first()


class Chapter(BaseModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.TextField(unique=True)

    objects = ChapterManager()

    class Meta:
        db_table = 'chapters'


class ServiceTypeManager(models.Manager):
    def get_by_pk(self, pk):
        return self.filter(pk=pk).first()


class ServiceType(BaseModel):
    service_type = models.CharField(max_length=255, choices=Choice.QUESTION_TYPE)

    objects = ServiceTypeManager()

    class Meta:
        db_table = 'service_types'


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

# class ServiceGeneratedManager(models.Manager):
#     pass


# class ServiceGenerated(BaseModel):
#     service_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
#     user = models.ForeignKey('user.User', on_delete=models.CASCADE, default=1)

#     objects = ServiceGeneratedManager()

#     class Meta:
#         db_table = 'services_generated'
