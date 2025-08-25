from django.urls import path, include
from django.views.generic.base import RedirectView
from .views import (
    AllChapterView,
    BoardView,
    GradeView,
    GradeAllSubjectView,
    SubjectAllChapterView,
    HomeView,
    ContentConfigurationView,
    QuestionTypeView,
    CustomDataView,
    GenerateQuestionView,
    DownloadContentView,
    GetLearningObjectiveView,
    LLMDescriptionView,
)


urlpatterns = [
    path('', RedirectView.as_view(url="home/")),
    path('home/', HomeView.as_view(), name="homepage"),
    path('fill-content-configuration/', ContentConfigurationView.as_view(), name='content-configuration'),
    path('fill-custom-data/', CustomDataView.as_view(), name='custom-data'),
    path('generate-questions/<int:pk>/', GenerateQuestionView.as_view(), name='generate-questions'),
    path('learning-objectives/<int:pk>', GetLearningObjectiveView.as_view(), name='get-learning-objective'),
    path('download-content/', DownloadContentView.as_view(), name='download-content'),
    path('llm-description/', LLMDescriptionView.as_view(), name=''),
    path('utils/', include([
            path('board/all/', BoardView.as_view(), name='boards-list'),
            path('grade/all/', GradeView.as_view(), name='grades-list'),
            path('grade/<int:pk>/subjects/', GradeAllSubjectView.as_view(), name='gradewise-subject-list'),
            path('subject/<int:pk>/chapters/', SubjectAllChapterView.as_view(), name='subjectwise-chapters-list'),
            path('chapter/all/', AllChapterView.as_view(), name='all-chapters'),
            path('question-type', QuestionTypeView.as_view(), name='question-type-list')
        ])
    ),
]
