from rest_framework.views import APIView
from .serializers import PromptSerializer, SubjectPromptSerializer, GradePromptSerializer
# from rest_framework.response import Response


class CreatePromptView(APIView):
    def post(self, request):
        serializer = PromptSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"code": 200, "message": "Done successfully"}


class SubjectPromptView(APIView):
    def post(self, request):
        serializer = SubjectPromptSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"code": 200, "message": "Created subject prompt successfully"}
    

class GradePromptView(APIView):
    def post(self, request):
        serializer = GradePromptSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"code": 200, "message": "Created grade prompt successfully"}