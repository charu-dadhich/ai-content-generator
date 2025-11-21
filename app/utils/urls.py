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
    ServiceView,
    CustomDataView,
    GenerateQuestionView,
    DownloadContentView,
    GetLearningObjectiveView,
    LLMDescriptionView,
    ServiceGradeView,
    GetActivityView,
)


urlpatterns = [
    path('', RedirectView.as_view(url="home/")),
    path('home/', HomeView.as_view(), name="homepage"),
    path('fill-content-configuration/', ContentConfigurationView.as_view(), name='content-configuration'),
    path('fill-custom-data/', CustomDataView.as_view(), name='custom-data'),
    path('generate-questions/<int:pk>/', GenerateQuestionView.as_view(), name='generate-questions'),
    path('learning-objectives/<int:pk>', GetLearningObjectiveView.as_view(), name='get-learning-objective'),
    path('activity/<int:pk>/', GetActivityView.as_view(), name='get-activity'),
    path('download-content/', DownloadContentView.as_view(), name='download-content'),
    path('llm-description/', LLMDescriptionView.as_view(), name=''),

    path('board/all/', BoardView.as_view(), name='boards-list'),#done
    path('grade/all/', GradeView.as_view(), name='grades-list'),#done
    path('grade/<int:pk>/subjects/', GradeAllSubjectView.as_view(), name='gradewise-subject-list'),#done
    path('board/<int:board_id>/subject/<int:subject_id>/chapters/', SubjectAllChapterView.as_view(), name='subjectwise-chapters-list'), #done
    path('chapter/all/', AllChapterView.as_view(), name='all-chapters'),#done
    path('services/', ServiceView.as_view(), name='services-list'), #done
    path('grade/<int:grade_id>/subject/<int:subject_id>/services/', ServiceGradeView.as_view(), name='grade-service') #done
]
