from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from app.base.models import BaseModel
from utils import Choice


class LearningObjectiveManager(models.Manager):
    def get_by_pk(self, pk):
        return self.filter(pk=pk).first()


class LearningObjective(BaseModel):
    description = models.TextField(default='')
    language = models.CharField(max_length=100, default='English')
    number_of_lo = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], default=10)
    standard = models.ForeignKey('utils.Standard', on_delete=models.CASCADE, null=True)
    board = models.ForeignKey('utils.Board', on_delete=models.CASCADE, null=True)
    chapter = models.ForeignKey('utils.Chapter', on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey('utils.ClassWiseSubject', on_delete=models.CASCADE, null=True)
    generation_type = models.CharField(max_length=20, default='custom', choices=Choice.GENERATION_TYPE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True)

    objects = LearningObjectiveManager()
    
    class Meta:
        db_table = 'learning_objectives'
