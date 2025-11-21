from rest_framework.views import APIView
from .serializers import (
    GenerateLearningSerializer,
    LearningObjectiveSerializer,
    ChangeLearningObjectiveSerializer,
)
from utils import Responder
from .models import LearningObjective


class CreateLearningObjectiveView(APIView):
    def post(self, request):
        serializer = GenerateLearningSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        learning_objective_object = serializer.save()
        data = LearningObjectiveSerializer(learning_objective_object).data
        data['content_type'] = 'Learning Objectives'
        data['service_type'] = 'Learning Objectives'
        return Responder.send(171, data)


class ChangeLearningObjectiveView(APIView):
    def _get_data(self, pk):
        if not (lo := LearningObjective.objects.get_by_pk(pk)):
            Responder.accept(174)
        return lo

    def patch(self, request, pk):
        lo = self._get_data(pk)
        serializer = ChangeLearningObjectiveSerializer(lo, data=request.data)
        serializer.is_valid(raise_exception=True)
        new_lo = serializer.save()
        data = LearningObjectiveSerializer(new_lo).data
        data['content_type'] = 'Learning Objectives'
        data['service_type'] = 'Learning Objectives'
        return Responder.send(175, data)
