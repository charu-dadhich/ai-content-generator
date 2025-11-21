from django.urls import path
from .views import (
    GenerateQuestionView,
    CustomQuestionTypeView,
    RegenerateQuestionView,
)


urlpatterns = [
    path('', GenerateQuestionView.as_view(), name="que-generator"),
    path('types/', CustomQuestionTypeView.as_view(), name="custom-question-types"),
    path('regenerate-question/', RegenerateQuestionView.as_view(), name='regenerate-question'),
]
