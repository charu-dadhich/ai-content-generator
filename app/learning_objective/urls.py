from django.urls import path
from .views import CreateLearningObjectiveView


urlpatterns = [
    path('', CreateLearningObjectiveView.as_view(), name='learning-objective'),
]