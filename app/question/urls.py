from django.urls import path
from .views import GenerateQuestionView, CustomQuestionTypeView


urlpatterns = [
    path('', GenerateQuestionView.as_view(), name="que-generator"),
    path('custom-types/', CustomQuestionTypeView.as_view(), name="custom-question-types")
]
