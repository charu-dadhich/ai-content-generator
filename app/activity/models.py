from django.db import models
from app.base.models import BaseModel
from utils.constants import Choice


class ActivityManager(models.Manager):
    def get_by_pk(self, pk):
        return self.filter(pk=pk).first()


class Activity(BaseModel):
    standard = models.ForeignKey('utils.Standard', on_delete=models.CASCADE, null=True)
    board = models.ForeignKey('utils.Board', on_delete=models.CASCADE, null=True)
    chapter = models.ForeignKey('utils.Chapter', on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey('utils.ClassWiseSubject', on_delete=models.CASCADE, null=True)
    generation_type = models.CharField(max_length=20, default='custom', choices=Choice.GENERATION_TYPE)
    activity_type = models.CharField(max_length=50, choices=Choice.ACTIVITY_TYPE)
    description = models.TextField(default='')
    language = models.CharField(max_length=100, default='English')
    activity_time_in_mins = models.IntegerField(default=15)
    sub_subject_name = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True)
    service_type = models.ForeignKey('utils.ServiceType', on_delete=models.CASCADE, null=True)

    objects = ActivityManager()

    class Meta:
        db_table = 'activities'
