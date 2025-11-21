from django.http import JsonResponse
from app.activity.serializers import ActivitySerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import TemplateView
from django.views import View
from app.question.serializers import QuestionAnswerSerializer, CustomQuestionTypeDetailSerializer, QuestionPaperSerializer
from utils.redis import Redis
from .serializers import (
    AllChapterSerializer, BoardSerializer, GradeSerializer, SubjectSerializer, ChapterSerializer, ServiceSerializer, BloomLevelSerializer, LLMDescriptionSerializer, ClassWiseSubjectSerializer)
from .models import Chapter, Board, ServiceGrade, Standard, Subject, ServiceType, BloomsLevel, ClassWiseSubject
from app.question.models import QuestionAnswer, CustomQuestionTypeDetail, QuestionPaper
from app.learning_objective.serializers import LearningObjectiveSerializer
from app.learning_objective.models import LearningObjective
import markdown
from django.utils.safestring import mark_safe
from utils import Responder
from app.activity.models import Activity
from question_ai.permissions import IsAuthenticated


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
        context["ques_data"] = ques_data
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
        html_content = mark_safe(markdown.markdown(text, extensions=['tables']))
        context["html"] = html_content
        context['step_number'] = 3
        context['total_steps'] = 4
        return context
    
    def extract_only_hindi(self, text):
        import re
        cleaned_text = re.sub(r'[a-zA-Z]', '', text)
        return cleaned_text

class GetActivityView(TemplateView):
    template_name = "activity.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        activity_id = self.kwargs.get('pk')
        activity = Activity.objects.get_by_pk(activity_id)
        serializer = ActivitySerializer(activity)
        data = serializer.data
        # context["data"]["description"] = self.extract_only_hindi(context["data"]["description"])
        raw_md = data["description"]
        import re
        text = re.sub(r':underline~~(.*?)~~', r'<u>\1</u>', raw_md)
        html_content = mark_safe(markdown.markdown(text, extensions=['tables']))
        context["html"] = html_content
        context['step_number'] = 3
        context['total_steps'] = 4
        return context
    

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
            35: {'name': QuestionPaper, 'serializer': QuestionPaperSerializer},
            12: {'name': QuestionPaper, 'serializer': QuestionPaperSerializer},
            15: {'name': QuestionPaper, 'serializer': QuestionPaperSerializer},
            36: {'name': Activity, 'serializer': ActivitySerializer}
        }
        service_class = service_classes_mapper.get(service_type_id)
        service_name = ServiceType.objects.get_by_pk(service_type_id).service_type
        resource = service_class['name'].objects.get_by_pk(resource_id)
        serializer = service_class['serializer'](resource)
        # else:
        #     question_paper = QuestionPaper.objects.filter(pk=resource_id).first()
        #     resource = service_class['name'].objects.get_by_question_paper_id(resource_id)
        #     serializer = service_class['serializer'](resource, many=True)
        #     context['']
        data = serializer.data
        # serializer = QuestionPaperSerializer(question_paper)
        # data = serializer.data
        context['step_number'] = 4
        context['data'] = data
        context['service_type'] = service_name
        return context


class ServiceView(View):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        services = ServiceType.objects.all()
        serializer = ServiceSerializer(services, many=True)
        data = serializer.data
        return Responder.send(151, data)


class BoardView(APIView):
    def get(self, request):
        if not (boards := Redis.get_key('all_boards')):
            boards = Board.objects.all()
            Redis.set_key('all_boards', boards, hours=720)
        serializer = BoardSerializer(boards, many=True)
        data = serializer.data
        return Responder.send(156, data)


class GradeView(APIView):
    def get(self, request):
        if not (grades := Redis.get_key('standards')):
            grades = Standard.objects.all()
            Redis.set_key('standards', grades, hours=720)
        serializer = GradeSerializer(grades, many=True)
        data = serializer.data
        return Responder.send(157, data)


class GradeAllSubjectView(APIView):
    def _get_data(self, pk):
        if not (standard := Standard.objects.get_by_pk(pk)):
            return Responder.accept(153)
        return standard

    def get(self, request, pk):
        standard = self._get_data(pk)
        if not (subjects := Redis.get_key(f'class_subjects_{pk}')):
            subjects = ClassWiseSubject.objects.get_by_standard(standard)
            Redis.set_key(f'class_subjects_{pk}', subjects, hours=720)
        serializer = ClassWiseSubjectSerializer(subjects, many=True)
        data = serializer.data
        return Responder.send(158, data)


class SubjectAllChapterView(APIView):
    def _get_data(self, subject_id, board_id):
        if not ClassWiseSubject.objects.get_by_pk(subject_id):
            return Responder.accept(153)
        if not Board.objects.get_by_pk(board_id):
            return Responder.accept(155)

    def get(self, request, board_id, subject_id):
        self._get_data(subject_id, board_id)
        # if not (chapters := Redis.get_key('subject_chapters')):
        chapters = Chapter.objects.get_by_subject_and_board(subject_id, board_id)
            # Redis.set_key('subject_chapters', chapters, hours=720)
        serializer = ChapterSerializer(chapters, many=True)
        data = serializer.data
        return Responder.send(154, data)


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


class ServiceGradeView(APIView):

    def _get_data(self, grade_id, subject_id):
        if not Standard.objects.get_by_pk(grade_id):
            return Responder.accept(152)
        services = ServiceGrade.objects.get_by_grade(grade_id)
        if not (subject := ClassWiseSubject.objects.get_by_pk(subject_id)):
            return Responder.accept(153)
        if subject.subject.name.lower() in ["english", "hindi", "sanskrit"]:
            services.exclude(service_type__service_type="Practice Progressive Section")
        return services

    def get(self, request, grade_id, subject_id):
        service_grades = self._get_data(grade_id, subject_id)
        services = [sg.service_type for sg in service_grades]
        serializer = ServiceSerializer(services, many=True)
        data = serializer.data
        return Responder.send(151, data)
