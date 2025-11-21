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



# class ServiceGeneratedManager(models.Manager):
#     pass


# class ServiceGenerated(BaseModel):
#     service_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
#     user = models.ForeignKey('user.User', on_delete=models.CASCADE, default=1)

#     objects = ServiceGeneratedManager()

#     class Meta:
#         db_table = 'services_generated'


# class BaseSubjectManager(models.Manager):
#     pass


# class BaseSubject(BaseModel):
#     name = models.CharField(max_length=255)

#     objects = BaseSubjectManager()

#     class Meta:
#         db_table = 'base_subjects'


