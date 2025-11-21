from rest_framework.views import APIView
from .serializers import (
    CreateActivitySerializer,
    ChangeActivitySerializer,
    ActivitySerializer,
)
from utils import Responder
from .models import Activity


class ActivityView(APIView):
    def post(self, request):
        serializer = CreateActivitySerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        activity = serializer.save()
        data = ActivitySerializer(activity).data
        data['content_type'] = 'Activity'
        data['blooms_taxonomy'] = []
        return Responder.send(181, data)


class ChangeActivityView(APIView):
    def _get_data(self, pk):
        if not (activity := Activity.objects.get_by_pk(pk)):
            Responder.accept(183)
        return activity

    def patch(self, request, pk):
        activity = self._get_data(pk)
        serializer = ChangeActivitySerializer(activity, data=request.data)
        serializer.is_valid(raise_exception=True)
        new_activity = serializer.save()
        data = ActivitySerializer(new_activity).data
        return Responder.send(182, data)
