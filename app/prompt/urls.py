from django.urls import path
from .views import (
    CreatePromptView,
    SubjectPromptView,
    GradePromptView
)


urlpatterns = [
    path('', CreatePromptView.as_view(), name='create_prompt'),
    path('subject-prompt/', SubjectPromptView.as_view(), name='subject_prompt'),
    path('grade-prompt/', GradePromptView.as_view(), name='grade_prompt')
]