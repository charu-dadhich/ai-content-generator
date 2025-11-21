from django.utils import timezone
from celery import shared_task
from datetime import timedelta
from .models import LearningObjective


@shared_task
def delete_learning_objectives_data():
    now = timezone.now()
    twenty_four_hours_ago = now - timedelta(hours=24)
    learning_objectives = LearningObjective.objects.filter(
        created_at__lte=twenty_four_hours_ago
    )
    learning_objectives.delete()
