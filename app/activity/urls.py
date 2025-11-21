from django.urls import path
from .views import (
    ActivityView,
    ChangeActivityView,
)


urlpatterns = [
    path('', ActivityView.as_view(), name='create-activity'),
    path('<int:pk>/', ChangeActivityView.as_view(), name='change-activity'),
]
