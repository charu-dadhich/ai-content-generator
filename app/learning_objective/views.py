from django.views import View
from .forms import LearningObjectiveForm
# from .serializers import CreateLearningObjectiveSerializer
# from django.http import JsonResponse
from utils import Responder


class CreateLearningObjectiveView(View):
    def post(self, request):
        form = LearningObjectiveForm(request.POST, request.FILES)
        if form.is_valid():
            print("inside if", form)
            lo = form.save()
            print("after save",lo)
            # serializer = CreateLearningObjectiveSerializer(lo)
            # data = serializer.data
            data = {}
            data['id'] = lo.id
            print("data", data)
            return Responder.send(100, data)
            # return JsonResponse({"status_code": 200, "data": data})
        else:
            print("Form errors:", form.errors)
            print("Non-field errors:", form.non_field_errors())
            # errors = form.errors + form.non_field_errors()
            # print("djjsjio",errors)
            for key, value in form.errors.items():
                errors = f"{key}: {value}"
            return Responder.error(100, errors)
            # return JsonResponse({"status_code": 400})
