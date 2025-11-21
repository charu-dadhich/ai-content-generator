from django.urls import path
from .views import (
    CreateLearningObjectiveView,
    ChangeLearningObjectiveView
)


urlpatterns = [
    path('', CreateLearningObjectiveView.as_view(), name='learning-objective'),
    path('<int:pk>/', ChangeLearningObjectiveView.as_view(), name='change-learning-objective'),
]
