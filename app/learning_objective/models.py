from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from app.base.models import BaseModel


class LearningObjectiveManager(models.Manager):
    def get_by_pk(self, pk):
        return self.filter(pk=pk).first()


class LearningObjective(BaseModel):
    description = models.TextField(default='')
    language = models.CharField(max_length=100, default='English')
    number_of_lo = models.IntegerField(validators = [MinValueValidator(1), MaxValueValidator(10)], default=10)
    standard = models.ForeignKey('base.Standard', on_delete=models.CASCADE, null=True)
    board = models.ForeignKey('base.Board', on_delete=models.CASCADE, null=True)
    chapter = models.ForeignKey('base.Chapter', on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey('base.Subject', on_delete=models.CASCADE, null=True)
    generation_type = models.CharField(max_length=20, default='custom')

    objects = LearningObjectiveManager()
    
    class Meta:
        db_table = 'learning_objectives'
