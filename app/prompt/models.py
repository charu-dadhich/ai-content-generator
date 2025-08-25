from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from app.base.models import BaseModel


class PromptManager(models.Manager):
    def get_by_service_type_id(self, service_type_id):
        print("service_type_id", service_type_id, self.filter(service_type_id=service_type_id).first())
        return self.filter(service_type_id=service_type_id).first()


class Prompt(BaseModel):
    # subject = models.ForeignKey('base.Subject', on_delete=models.CASCADE)
    description = models.TextField()
    temperature = models.FloatField(default=0.6, validators = [MinValueValidator(1), MaxValueValidator(10)])
    user = models.ForeignKey('user.User', on_delete=models.SET_DEFAULT, default=1)
    service_type = models.ForeignKey('base.ServiceType', on_delete=models.CASCADE)
    model = models.ForeignKey('base.LLMModel', on_delete=models.CASCADE, null=True)

    objects = PromptManager()

    class Meta:
        db_table = 'prompts'


class SubjectSpecificPromptManager(models.Manager):
    def get_by_prompt_and_subject_id(self, prompt, subject_id):
        print(prompt, subject_id)
        print(self.filter(prompt=prompt, subject_id=subject_id).first())
        return self.filter(prompt=prompt, subject_id=subject_id).first()


class SubjectSpecificPrompt(BaseModel):
    prompt = models.ForeignKey('Prompt', on_delete=models.CASCADE, related_name='subject_specific_prompts')
    subject = models.ForeignKey('base.Subject', on_delete=models.CASCADE, related_name='subject_prompts')
    description = models.TextField(null=True, blank=True)

    objects = SubjectSpecificPromptManager()

    class Meta:
        db_table = 'subject_specific_prompts' 


class GradeSpecificPromptManager(models.Manager):
    def get_by_prompt_and_grade_id(self, prompt, grade_id):
        return self.filter(prompt=prompt, standard_id=grade_id).first()


class GradeSpecificPrompt(BaseModel):
    prompt = models.ForeignKey('Prompt', on_delete=models.CASCADE, related_name='grade_specific_prompts')
    standard = models.ForeignKey('base.Standard', on_delete=models.CASCADE, related_name='grade_prompts')
    description = models.TextField(null=True, blank=True)

    objects = GradeSpecificPromptManager()

    class Meta:
        db_table = 'grade_specifc_prompts'


# class PromptDetail(BaseModel):
#     prompt = models.ForeignKey('Prompt', on_delete=models.CASCADE)
#     class_start_id = models.ForeignKey('base.Standard', on_delete=models.CASCADE, related_name='prompt_detail_class_start')
#     class_end_id = models.ForeignKey('base.Standard', on_delete=models.CASCADE, related_name='prompt_detail_class_end')
#     subject = models.ForeignKey('base.subject', on_delete=models.CASCADE, related_name='')