from django.views import View
from django.http import JsonResponse
from django.db import transaction
from django.conf import settings
from app.base.models import ServiceType
from .forms import GeneratedQuestionForm
from .serializers import QuestionAnswerSerializer, CustomQuestionTypeDetailSerializer
from .models import QuestionAnswer, QuestionPaper, DetailQuestionPaperScheme, CustomQuestionTypeDetail
from utils.gpt import CustomAI
import json
import re
import demjson3


class GenerateQuestionView(View):

    def post(self, request):
        # import json
        print(request.FILES)
        print(request.POST)
        ifile = request.FILES.get('file_input')
        print(ifile)
        # data = json.loads(request.body)
        # print("data----->", data)
        form = GeneratedQuestionForm(request.POST, request.FILES)
        if form.is_valid():
            # cleaned_data = form.cleaned_data
            question_paper, answers = form.save()
            serializer = QuestionAnswerSerializer(answers, many=True)
            ques_data = serializer.data
            response_data = {
                'question_paper_id': question_paper.id,
                'total_questions': question_paper.total_questions,
                'questions_data': ques_data
            }
            print(response_data)
            return JsonResponse({"status_code": 200, "data": response_data})
        else:
            print("Form errors:", form.errors)
            print("Non-field errors:", form.non_field_errors())
            return JsonResponse({"status_code": 400})
        # return JsonResponse({"status_code": 400})

            # question_paper_attrs = {
            #     'standard_id': cleaned_data.get('grade'),
            #     'board_id': cleaned_data.get('board'),
            #     'subject_id': cleaned_data.get('subject'),
            #     'chapter_id': cleaned_data.get('chapter'),
            #     'language': cleaned_data.get('language'),
            #     'topic': cleaned_data.get('topic'),
            #     'sub_topic': cleaned_data.get('sub_topic'),
            #     'generation_type': cleaned_data.get('generation_type'),
            #     'total_questions': cleaned_data.get('total_questions') or 15,
            #     'blooms_taxonomy': cleaned_data.get('bloom_filters') or []
            # }
            # print("attrs", question_paper_attrs, question_paper_attrs['generation_type'] == "auto")
            # file_path = cleaned_data.get('custom_file_path')
            # ai = CustomAI(file_path)
            # user_prompt = '''Generate questions based on class {question_paper_attrs.get('standard_id')} cbse subject {cleaned_data.get('subject_name')} and chapter cleaned_data.get('chapter_name')'''
            # if ans := ai.generate_questions(user_prompt, cleaned_data, question_paper_attrs):
            #     print(ans)
            #     with transaction.atomic():
            #         question_paper = QuestionPaper.objects.create(**question_paper_attrs)
            #         paper_scheme_attrs = {
            #             'total_one_mark_questions': settings.DEFAULT_ONE_MARK_QUESTIONS,
            #             'total_two_mark_questions': settings.DEFAULT_TWO_MARK_QUESTIONS,
            #             'total_four_mark_questions': settings.DEFAULT_FOUR_MARK_QUESTIONS,
            #             'one_mark_answer_word_count': 50,
            #             'two_mark_answer_word_count': 100,
            #             'four_mark_answer_word_count': 200,
            #             'question_paper': question_paper
            #         }
                    # paper_scheme = DetailQuestionPaperScheme.objects.create(**paper_scheme_attrs)
                    

                    # def extract_json(response):
                    #     match = re.search(r'\[\s*{.*?}\s*]', response, re.DOTALL)
                    #     if match:
                    #         raw_json = match.group()

                    #         # Fix common LLM issues: trailing commas, backslashes, etc.
                    #         raw_json = re.sub(r',(\s*[}\]])', r'\1', raw_json)  # Remove trailing commas
                    #         raw_json = raw_json.replace('\\"', '"')             # Replace escaped quotes
                    #         raw_json = raw_json.replace('\\n', '\n')            # Fix line breaks if needed
                    #         raw_json = raw_json.replace('\\t', '\t')            # Fix tabs if needed
                    #         try:
                    #             # return json.loads(raw_json)
                    #             return demjson3.decode(raw_json)
                    #         except json.JSONDecodeError as e:
                    #             print("JSON decoding error:", e)
                    #             print("Sanitized JSON string:")
                    #             print(raw_json)
                    #             return None
                    #     return None
                    # def extract_json(response):
                    #     # Extract JSON array of objects from the text (non-greedy)
                    #     match = re.search(r'\[\s*{.*?}\s*\]', response, re.DOTALL)
                    #     if not match:
                    #         return None

                    #     raw_json = match.group()

                    #     # Fix common issues:
                    #     # 1. Remove trailing commas before } or ]
                    #     raw_json = re.sub(r',(\s*[}\]])', r'\1', raw_json)

                    #     # 2. Escape unescaped backslashes that cause invalid \escape errors
                    #     #    Only keep valid JSON escape sequences unescaped
                    #     # This regex finds a backslash not followed by valid JSON escape chars
                    #     raw_json = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', raw_json)

                    #     # 3. Optionally fix escaped quotes (if incorrectly escaped)
                    #     raw_json = raw_json.replace('\\"', '"')

                    #     # 4. Fix literal \n and \t to real newlines and tabs (optional)
                    #     raw_json = raw_json.replace('\\n', '\n').replace('\\t', '\t')

                    #     try:
                    #         return json.loads(raw_json)
                    #     except json.JSONDecodeError as e:
                    #         print("JSON decoding error:", e)
                    #         print("Sanitized JSON string:")
                    #         print(raw_json)
                    #         return None



                    # def extract_json(ans):
                    #     cleaned_text = re.sub(r"```json\s*([\s\S]*?)```", r"\1", ans, flags=re.MULTILINE)

                    #     # If the above doesn't catch, also try removing any backticks wrapping whole string
                    #     cleaned_text = cleaned_text.strip('` \n\r\t')

                    #     # Now parse cleaned JSON string
                    #     try:
                    #         data = demjson3.decode(cleaned_text)
                    #         return data
                    #     except Exception as e:
                    #         print(f"Error parsing JSON: {e}")
                    #         return None

                    # res = extract_json(ans)
                    # print("extracted json--------------------", res)



                    # clean_json = ans.replace("json", "").replace("", "").strip()

                    # print("cleaned json", clean_json)
                    # try:
                    #     res = demjson3.decode(clean_json)
                    #     print("*************************")
                    #     print(res)
                    # except demjson3.JSONDecodeError as e:
                    #     print("Failed to parse JSON:", e)
                    # questions = []
                    # if res:
                    #     for r in res:
                    #         r['detail'] = r.pop('question', '')
                    #         r.pop('question_number', '')
                    #         r.pop('answer_word_count', '')
                    #         type_name = r.pop('type_of_question', '')
                    #         if type := QuestionType.objects.filter(type=type_name).first():
                    #             r['type'] = type
                    #         else:
                    #             r['type_id'] = 1
                    #         r['correct_answer'] = r.pop('correct_option', '')
                    #         r['question_paper'] = question_paper
                    #         questions.append(QuestionAnswer.objects.create(**r))
                        # question_answers = QuestionAnswer.objects.bulk_create(questions)
                #         serializer = QuestionAnswerSerializer(questions, many=True)
                #         ques_data = serializer.data
                #         response_data = {
                #             'question_paper_id': question_paper.id,
                #             'total_questions': question_paper.total_questions,
                #             'questions_data': ques_data
                #         }
                #         print(response_data)
                #         return JsonResponse({"status_code": 200, "data": response_data})
                # return JsonResponse({"status_code": 400})
        


class CustomQuestionTypeView(View):

    def get(self, request):
        question_types = CustomQuestionTypeDetail.objects.get_all()
        serializer = CustomQuestionTypeDetailSerializer(question_types, many=True)
        data = serializer.data
        print(data)
        return JsonResponse({'data': data, 'status_code': 200, 'status': True})
