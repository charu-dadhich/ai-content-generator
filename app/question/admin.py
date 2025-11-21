from django.contrib import admin
from .models import (
    QuestionPaper,
    CustomQuestionTypeDetail
)


admin.site.register(QuestionPaper)
admin.site.register(CustomQuestionTypeDetail)
