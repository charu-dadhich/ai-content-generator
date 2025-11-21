from django.utils import timezone
from celery import shared_task
from datetime import timedelta
from .models import Activity


@shared_task
def delete_activities_data():
    now = timezone.now()
    twenty_four_hours_ago = now - timedelta(hours=24)
    activities = Activity.objects.filter(
        created_at__lte=twenty_four_hours_ago
    )
    activities.delete()
