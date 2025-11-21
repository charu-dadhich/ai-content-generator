
from openai import OpenAI
from django.conf import settings
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import traceback
from .helper import Helper
from .responder import Responder
from .logger import Logger


class CustomAI():
    def __init__(self, pdf_path=''):
        # Load and split PDF
        if pdf_path:
            loader = PyMuPDFLoader(pdf_path)
            documents = loader.load()
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            docs = text_splitter.split_documents(documents)

        # Create vector store
            embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            self.db = Chroma.from_documents(docs, embedding)

        # Store OpenAI client
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.API_KEY,
        )

    def chat_api(self, final_prompt):
        try:
            completion = self.client.chat.completions.create(
                # model="qwen/qwq-32b:free",
                # model="deepseek/deepseek-r1-distill-llama-70b:free",
                model="deepseek/deepseek-r1-0528-qwen3-8b:free",
                # model="mistralai/mistral-small-3.2-24b-instruct:free",
                # model="moonshotai/kimi-dev-72b:free",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                'text': final_prompt,
                                'type': "text"
                            },
                            {
                                'type': "image",
                                'image': "image.png"
                            }
                        ]
                    }
                ]
            )
            if not completion or not hasattr(completion, "choices") or not completion.choices:
                # Logger.error()
                Responder.accept(191)
                # raise ValueError("No choices returned from model.")
            message = completion.choices[0].message
            if not message or not hasattr(message, "content"):
                # Logger.error()
                # raise ValueError("No message content in the first choice.")
                Responder.accept(191)
            # Get token usage from response
            print(f"Input tokens: {completion.usage.prompt_tokens}")
            print(f"Output tokens: {completion.usage.completion_tokens}")
            print(f"Total tokens: {completion.usage.total_tokens}")
            return message.content

        except Exception as e:
            print(traceback.format_exc())
            print(f"Error in chat_api: {e}")
            # Logger.error()
            Responder.accept(191)

    def generate_questions(self, user_prompt, cleaned_data, question_paper_attrs):
        # relevant_docs = self.db.similarity_search(user_prompt, k=5)
        # retrieved_text = "\n".join([doc.page_content for doc in relevant_docs])
        service_type_id = cleaned_data.pop('service_type_id', '')
        final_args = {}
        from app.prompt.models import Prompt, PromptDetail
        if service_type_id not in [19, 36]:
            format_args = {}
            if question_paper_attrs['generation_type'] != "auto":
                QUESTION_TYPE_LABELS = {
                    "mcqs": "Multiple Choice Questions",
                    "short_answer": "Short Answer Questions",
                    "long_answer": "Long Answer Questions",
                    "application_based": "Application Based Questions",
                    "assertion_reason": "Assertion & Reason Questions",
                    "reference_to_context": "Reference to Context Questions",
                    "statement_based": "Statement Based Questions",
                    "source_based": "Source Based Questions",
                    "parallel": "Parallel Questions",
                    "writing_skill": "Writing Skill Based Questions",
                    "case_based": "Case Based Questions",
                    "paragraph_based": "Paragraph Based Questions",
                    "fill_in_the_blanks": "Fill in the Blanks Questions",
                    "match_the_following": "Match the Following Questions",
                    "critical_analysis": "Critical Analysis Based Questions",
                    "if_based": "If Based Questions",
                }
                question_type_data = {}
                for qtype in QUESTION_TYPE_LABELS.keys():
                    raw_value = cleaned_data.get(qtype)
                    print("RAW_VALUE", raw_value, qtype)
                    if raw_value:
                        try:
                            question_type_data[qtype] = raw_value
                        except Exception as e:
                            question_type_data[qtype] = {}
                question_type_lines = []
                for qtype in QUESTION_TYPE_LABELS.keys():
                    print("question type", question_type_data)
                    data = question_type_data.get(f"{qtype}", {})
                    print(data)
                    if isinstance(data, list):
                        print("in")
                        for item in data:
                            print(data, item)
                            format_args[f"{qtype}_number_of_questions"] = item.get("number_of_questions", 0)
                            format_args[f"{qtype}_marks_per_question"] = item.get("marks_per_question", 1)
                            format_args[f"{qtype}_total_sub_questions"] = item.get("total_sub_questions", 0)
                            format_args[f"{qtype}_sub_subjective_questions"] = item.get("sub_subjective_questions", 0)
                            format_args[f"{qtype}_sub_objective_questions"] = item.get("sub_objective_questions", 0)
                            format_args[f"{qtype}_sub_objective_questions"] = item.get("sub_objective_questions", 0)
                            num = item.get("number_of_questions", 0)
                            marks = item.get("marks_per_question", 1)
                            total_sub_questions = item.get("total_sub_questions")
                            sub_subjective_questions = item.get("sub_subjective_questions", 0)
                            sub_objective_questions = item.get("sub_objective_questions", 0)
                            marks_per_subjective_question = item.get("marks_per_subjective_question", 2)
                            marks_per_objective_question = item.get("marks_per_objective_question", 1)
                            word_limit = item.get("word_limit", 0)
                            if num > 0:
                                label = QUESTION_TYPE_LABELS.get(qtype, qtype.replace("_", " ").title())
                                if item.get('number_of_questions'):
                                    if total_sub_questions:
                                        question_type_lines.append(f"- {num} {label}, each carrying {marks} mark(s) with {total_sub_questions} sub-questions each, ({sub_subjective_questions} Subjective sub questions each with marks {marks_per_subjective_question} having answer word limit {word_limit}, {sub_objective_questions} Objective sub questions each with marks {marks_per_objective_question})")
                                    else:
                                        question_type_lines.append(f"- {num} {label}, each carrying {marks} mark(s) having answer word_limit {word_limit}")
                    else:
                        format_args[f"{qtype}_number_of_questions"] = data.get("number_of_questions", 0)
                        format_args[f"{qtype}_marks_per_question"] = data.get("marks_per_question", 1)
                        format_args[f"{qtype}_total_sub_questions"] = data.get("total_sub_questions", 0)
                        format_args[f"{qtype}_sub_subjective_questions"] = data.get("sub_subjective_questions", 0)
                        format_args[f"{qtype}_sub_objective_questions"] = data.get("sub_objective_questions", 0)
                        format_args[f"{qtype}_word_limit"] = data.get("word_limit", 0)
                        num = data.get("number_of_questions", 0)
                        marks = data.get("marks_per_question", 1)
                        total_sub_questions = data.get("total_sub_questions")
                        sub_subjective_questions = data.get("sub_subjective_questions", 0)
                        sub_objective_questions = data.get("sub_objective_questions", 0)
                        word_limit = data.get("word_limit", 0)
                    
                        if num > 0:
                            label = QUESTION_TYPE_LABELS.get(qtype, qtype.replace("_", " ").title())
                            if data.get('number_of_questions'):
                                if total_sub_questions:
                                    question_type_lines.append(f"- {num} {label}, each carrying {marks} mark(s) with {total_sub_questions} sub-questions each, ({sub_subjective_questions} Subjective sub questions each with marks {marks_per_subjective_question} having answer word limit {word_limit}, {sub_objective_questions} Objective sub questions each with marks {marks_per_objective_question})")
                                else:
                                    question_type_lines.append(f"- {num} {label}, each carrying {marks} mark(s) having answer word_limit {word_limit}")
                final_args["question_type_block"] = "\n".join(question_type_lines) if question_type_lines else "No questions specified."
            else:
                cleaned_data['total_questions'] = 5
                final_args["question_type_block"] = """- 1 Mulitple Choice Questions, each carrying 1 mark
                    - 1 Fill in the blanks, each carrying 1 mark,
                    - 1 Short Answer Questions with word limit upto 200 each carrying 3 marks,
                    - 2 Long Answer Questions with word limit upto 500 each carrying 4 marks
                    - No any other question type like Statement Based, case Based, Assertion Reason, Paragraph based, Source Based, etc to be framed apart from mentioned above
                """

        if service_prompt := Prompt.objects.get_by_service_type_id(service_type_id):
            # if service_type_id in [1, 2]:
            #     context_block = f"""
            #         === BEGIN CHAPTER CONTENT ===
            #         {cleaned_data.get('retrieved_text')}
            #         === END CHAPTER CONTENT ===
            #         """
            final_prompt = service_prompt.description.format(
                total_questions=15,
                class_name=cleaned_data.get('standard_id'),
                board_name=cleaned_data.get('board_id'),
                subject_name=cleaned_data.get('subject_name'),
                chapter_name=cleaned_data.get('chapter_name'),
                number_of_lo=cleaned_data.get('number_of_lo') or 10,
                topic=cleaned_data.get('topic'),
                sub_topic=cleaned_data.get('sub_topic'),
                easy_percentage=cleaned_data.get('easy_percentage', 30),
                medium_percentage=cleaned_data.get('medium_percentage', 30),
                difficult_percentage=cleaned_data.get('difficult_percentage', 30),
                very_challenging_percentage=cleaned_data.get('very_challenging_percentage', 10),
                sub_subject_name=cleaned_data.get('sub_subject_name', ''),
                activity_time_in_mins=cleaned_data.get('activity_time_in_mins') or 15,
                retrieved_text=cleaned_data.get('retrieved_text'),
                **final_args
            )
            from app.utils.models import Subject
            base_subject_id = Subject.objects.filter(name=cleaned_data.get('subject_name')).first()
            if prompt_detail := PromptDetail.objects.get_by_prompt_class_subject(service_prompt, cleaned_data.get('standard_id'), base_subject_id):
                final_prompt = final_prompt.replace("__SUBJECT_SPECIFIC_GUIDELINES__", prompt_detail.description)
            fp = Helper.generate_final_prompt(service_prompt.service_type.service_type, cleaned_data.get('standard_id'), cleaned_data.get('subject_name'), final_prompt)
            print("final prompt", fp)
            ans = self.chat_api(fp)
            print(ans)
            return ans
