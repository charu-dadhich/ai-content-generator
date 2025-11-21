from django.utils import timezone
from celery import shared_task
from datetime import timedelta
from .models import QuestionPaper


@shared_task
def delete_questions_data():
    now = timezone.now()
    twenty_four_hours_ago = now - timedelta(hours=24)
    question_papers = QuestionPaper.objects.filter(
        created_at__lte=twenty_four_hours_ago
    )
    question_papers.delete()
