from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import TemplateView
from django.views import View
from app.question.serializers import QuestionAnswerSerializer, CustomQuestionTypeDetailSerializer, QuestionPaperSerializer
from .serializers import (
    AllChapterSerializer, BoardSerializer, GradeSerializer, SubjectSerializer, ChapterSerializer, ServiceTypeSerializer, BloomLevelSerializer, LLMDescriptionSerializer)
from .models import Chapter, Board, Standard, Subject, ServiceType, BloomsLevel
from app.question.models import QuestionAnswer, CustomQuestionTypeDetail, QuestionPaper
from app.learning_objective.serializers import CreateLearningObjectiveSerializer
from app.learning_objective.models import LearningObjective
import markdown
from django.utils.safestring import mark_safe
from utils import Responder


# class AllChapterView(TemplateView):
#     def get(self, request):
#         chapters = Chapter.objects.all()
#         serializer = AllChapterSerializer(chapters, many=True)
#         data = serializer.data
#         print(data)
#         return Response(data)


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["disable_previous"] = True
        context["next_page"] = 'content-configuration'
        context['step_number'] = 1
        context['total_steps'] = 4
        return context


class ContentConfigurationView(TemplateView):
    template_name = "content.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["disable_previous"] = False
        context['previous_page'] = 'home'
        context["next_page"] = 'generate-questions'
        context['step_number'] = 2
        context['total_steps'] = 4
        return context



class CustomDataView(TemplateView):
    template_name = "dynamic_configuration.html"
    # @ensure_csrf_cookie
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_types = CustomQuestionTypeDetail.objects.get_all()
        serializer = CustomQuestionTypeDetailSerializer(question_types, many=True)
        question_types = serializer.data
        bloom_levels = BloomsLevel.objects.all()
        bloom_level_serializer = BloomLevelSerializer(bloom_levels, many=True)
        bloom_levels = bloom_level_serializer.data
        context["previous_page"] = 'content-configuration'
        context["next_page"] = 'generate-questions'
        context['step_number'] = 3
        context['total_steps'] = 5
        context['question_types'] = question_types
        context['bloom_levels'] = bloom_levels
        return context


class GenerateQuestionView(TemplateView):
    template_name = "generate_questions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        generation_type = self.request.GET.get('generation_type')
        context['step_number'] = 3
        context['total_steps'] = 5
        if generation_type == "auto":
            context['step_number'] = 3
            context['total_steps'] = 4
        question_paper_id = self.kwargs.get('pk')
        question_answers = QuestionAnswer.objects.get_by_question_paper_id(question_paper_id)
        serializer = QuestionAnswerSerializer(question_answers, many=True)
        ques_data = serializer.data
        # context["next_page"] = 'content-configuration'
        print("in viw", ques_data)
        context["ques_data"] = ques_data
        print("ques_daa", ques_data)
        return context


class GetLearningObjectiveView(TemplateView):
    template_name = "learning_objective.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        learning_objective_id = self.kwargs.get('pk')
        learning_objective = LearningObjective.objects.get_by_pk(learning_objective_id)
        serializer = CreateLearningObjectiveSerializer(learning_objective)
        data = serializer.data
        # context["data"]["description"] = self.extract_only_hindi(context["data"]["description"])
        raw_md = data["description"]
        import re
        text = re.sub(r':underline~~(.*?)~~', r'<u>\1</u>', raw_md)
        print("text after underlinign", text)
        html_content = mark_safe(markdown.markdown(text, extensions=['tables']))
        # print("html",html_content)
        context["html"] = html_content
        context['step_number'] = 3
        context['total_steps'] = 4
        return context
    
    def extract_only_hindi(self, text):
        import re
        cleaned_text = re.sub(r'[a-zA-Z]', '', text)
        return cleaned_text


class DownloadContentView(TemplateView):
    template_name = "download_content.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # question_paper_id = self.kwargs.get('pk')
        service_type_id = int(self.request.GET.get('service_type_id', 12))
        resource_id = self.request.GET.get('resource_id', 1)
        service_classes_mapper = {
            19: {'name': LearningObjective, 'serializer': CreateLearningObjectiveSerializer},
            18: {'name': QuestionPaper, 'serializer': QuestionPaperSerializer},
            17: {'name': QuestionPaper, 'serializer': QuestionPaperSerializer},
        }
        print(service_type_id, service_classes_mapper.get(19), type(service_type_id))
        service_class = service_classes_mapper.get(service_type_id)
        print(service_class)
        service_name = ServiceType.objects.get_by_pk(service_type_id).service_type
        print("serv9ce name", service_name)
        # if service_class['name'] == LearningObjective:
        resource = service_class['name'].objects.get_by_pk(resource_id)
        serializer = service_class['serializer'](resource)
        # else:
        #     question_paper = QuestionPaper.objects.filter(pk=resource_id).first()
        #     resource = service_class['name'].objects.get_by_question_paper_id(resource_id)
        #     serializer = service_class['serializer'](resource, many=True)
        #     context['']
        data = serializer.data
        print(serializer.data)
        # serializer = QuestionPaperSerializer(question_paper)
        # data = serializer.data
        context['step_number'] = 4
        context['data'] = data
        context['service_type'] = service_name
        return context


class QuestionTypeView(View):
    def get(self, request):
        if question_types := ServiceType.objects.all():
            serializer = ServiceTypeSerializer(question_types, many=True)
            data = serializer.data
            # print()
            return JsonResponse({'data': data, 'status_code': 200, 'status': True})
   

class BoardView(View):
    def get(self, request):
        if boards := Board.objects.all():
            serializer = BoardSerializer(boards, many=True)
            data = serializer.data
            return JsonResponse({'data': data, 'status_code': 200, 'status': True})


class GradeView(View):
    def get(self, request):
        if grades := Standard.objects.all():
            serializer = GradeSerializer(grades, many=True)
            data = serializer.data
            return JsonResponse({'data': data, 'status_code': 200, 'status': True})
        

class GradeAllSubjectView(View):
    def _get_data(self, pk):
        if not (standard := Standard.objects.get_by_pk(pk)):
            return JsonResponse({'data':{}, 'status':False, 'status_code':400})
        return standard
    
    def get(self, request, pk):
        standard = self._get_data(pk)
        subjects = Subject.objects.get_by_standard(standard)
        serializer = SubjectSerializer(subjects, many=True)
        data = serializer.data
        return JsonResponse({'data': data, 'status_code': 200, 'status': True})


class SubjectAllChapterView(View):
    def _get_data(self, pk):
        if not (subject := Subject.objects.get_by_pk(pk)):
            return JsonResponse({'data':{}, 'status':False, 'status_code':400})
        return subject

    def get(self, request, pk):
        subject = self._get_data(pk)
        chapters = Chapter.objects.get_by_subject(subject)
        serializer = ChapterSerializer(chapters, many=True)
        data = serializer.data
        return JsonResponse({'data': data, 'status_code': 200, 'status': True})


class AllChapterView(APIView):
    def get(self, request):
        chapters = Chapter.objects.all()
        serializer = AllChapterSerializer(chapters, many=True)
        data = serializer.data
        return Response(data)


class LLMDescriptionView(APIView):
    def post(self, request):
        serializer = LLMDescriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = LLMDescriptionSerializer.data
        return JsonResponse({'data': data, 'status_code': 200, 'status': True})
