from openai import OpenAI
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import traceback
from .helper import Helper



class CustomAI():
    def __init__(self, pdf_path):
        # Load and split PDF
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
            api_key="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",
        )
    
        self.prompt = """You are to generate questions strictly in JSON format.

            Instructions:
            - Frame exactly {number_of_questions} questions.No more or less than {number_of_questions} questions should be generated.
            - Include:
                - {subjective_2_marks} two marks subjective short answer questions exactly
                - {subjective_4_marks} four marks subjective long answer questions exactly
                - {objective_2_options} one mark objective questions with 2 options exactly
                - {objective_4_options} one mark objective questions with 4 options exactly
                - {case_based} four marks case based questions exactly
                - {fill_ups} one mark fill in the blanks questions exactly
                - {match_ups} one mark match ups questions exactly
                - Generate question paper in {language} language exactly
                - No MCQ with three options should be there.

            - All content must be based on this retrieved text {retrieved_text}.
            - Take Topic as {topic}
            - Take sub topic as {sub_topic}
            - Any question which belongs to the any of the value or all from {{blooms_taxonomy}} , bloom filters
            - Ensure that the overall difficulty distribution of the questions is as follows:
                - {easy_percentage}% Easy: Basic recall or direct questions
                - {medium_percentage}% Moderate: Involve some reasoning or conceptual understanding
                - {difficult_percentage}% Difficult: Require deep understanding or multi-step reasoning
                - {very_challenging_percentage}% Very Challenging: Designed to test higher-order thinking or critical analysis
            - Keep the question paper level according to class. Don't go above that. For lower classes like from class 1 to 5, keep the language simple and very book specific.
            - For maths or mathematics subject, take 2 marks and 4 marks as numericals or to prove questions strictly. No theory question to explain something or definitions kind of shoule be there.
            - For hindi and sanskrit subjects keep the generation language as hindi and sanskrit respectively.
            - For Chemistry, Physics or Science subjects for classes 9, 10, 11, 12 frame 30% of numericals also in paper. 
            - Chapter Content for reference - {retrieved_text}
            - Always try to generate based on the retrieved text. Always cover the entire chapter and generate questions from different topics, if topic is not given.
            - For class 9, 10, 11, 12:
                - Two-mark answers: 80–140 words
                - Four-mark answers: Minimum 400 words, and should include placeholders like [Image: XYZ diagram] or [Table: Comparison of A vs B] wherever needed
            - In answer explanation, you need to write the answer for theory questions, calculation for numerical questions and reason to supposrt answer in case of objective questions
            - Always stick to the instructions, no more or less than the specified number of questions should be generated
            - Also, exact type of questions should be generated. For example, if no fill in the blanks is there or if it is 0 then, no question of type fill in the blanks should be generated.

            Question Types:
            1. One-mark Questions:
                - Should test recall and basic understanding.
                - Correct option must be specified in case of MCQs.
                - Correcct matching options should be there in match the following.
            2. Two-mark questions:
                - Test ability to elaborate or explain concepts.
                - Answers should be 50–80 words.
            3. Four-mark questions and Case based questions:
                - Test critical thinking or deeper understanding.
                - Answers should be 150–350 words.

            Output Format:
            - Only return the JSON array. Do not include any explanation, introduction, summary, or extra text.
            - Do not include characters which could not be parsed as python dictionary data type
            - DO not include in value any kind of semi-colon(:) or double-quotes, try to use single quotes i fthere is some sentenc inside value pairs. For example- 
                {{
                    "answer_explanation": "This is called 'Light'"
                }}

            [
                {{
                    "question_number": 1,
                    "question": "",
                    "type_of_question": ["theory",
                        "numerical,
                        "MCQ",
                        "CBQ",
                        "CET",
                        "LO",
                        "Learning Journey",
                        "Activity Based Learning,
                        "Translation"]
                    "options": {{"a": "Option 1", "b": "Option 2", "c": "Option 3", "d": "Option 4"}},  // Include only for Objective
                    "correct_option": "a",  // Leave blank for Subjective
                    "answer_explanation": "",
                    "learning_outcome": "",
                    "answer_word_count": // Should be an integer numer as per the answer count genearted,
                    "difficulty_level": "" // Should be a value from easy, medium or moderate and difficult,
                    "marks": //Integer or float value upto one decimal place,
                    "blooms_taxonomy": //Any value from given {{blooms_taxonomy}} from which the question belongs to.
                }},
            ]
        """

        self.auto_generate_questions_prompt = """
            You are to generate questions strictly in JSON format.

            Instructions:
            - Frame exactly {number_of_questions} questions. No more or less than {number_of_questions} questions should be generated.
            - Include:
                - {number_of_one_mark_questions} one-mark multiple choice questions (MCQs)
                - {number_of_two_mark_questions} two-mark short answer questions
                - {number_of_four_mark_questions} four-mark long answer questions
            - All content must be based on the NCERT {board_name} board, Class {class_name}, Subject: {subject_name}, Chapter: {chapter_name}.
            - Ensure that the overall difficulty distribution of the questions is as follows:
                -- 25% Easy: Basic recall or direct questions
                -- 50% Moderate: Involve some reasoning or conceptual understanding
                -- 20% Difficult: Require deep understanding or multi-step reasoning
                -- 5% Very Challenging: Designed to test higher-order thinking or critical analysis
            - Keep the question paper level according to class. Don't go above that. For lower classes like from class 1 to 5, keep the language simple and very book specific.
            - For maths or mathematics subject, take 2 marks and 4 marks as numericals or to prove questions strictly. No theory question to explain something or definitions kind of shoule be there.
            - For Hindi subject:
                - All questions and answers must be written only in Hindi.
                - Do not include any English or mixed-language content.
                - Use only the uploaded chapter content.
                - Do not introduce any external content, character names, author names, or settings not present in the uploaded text.
                - Preserve all names and story details exactly as in the original text — no alterations.
            - For Chemistry, Physics or Science subjects for classes 9, 10, 11, 12 frame 30% of numericals also in paper. 
            - Chapter Content for reference - {retrieved_text}
            - Always try to generate based on the retrieved text. Always cover the entire chapter and generate questions from different topics, if topic is not given.
            - For class 9, 10, 11, 12:
                - Two-mark answers: 80–140 words
                - Four-mark answers: Minimum 400 words, and should include placeholders like [Image: XYZ diagram] or [Table: Comparison of A vs B] wherever needed.
            - In answer explanation, you need to write the answer for theory questions, calculation for numerical questions and reason to supposrt answer in case of objective questions.
            - Do not ever keep question and answer_explanation empty.
            - Always generate questions for hindi and english from the chapter content uploaded without changing name of characters and story. 

            Question Types:
            1. One-mark MCQs:
                - Should test recall and basic understanding.
                - Must have 4 options labeled a, b, c, d.
                - Correct option must be specified.
            2. Two-mark questions:
                - Test ability to elaborate or explain concepts.
                - Answers should be 50–80 words.
            3. Four-mark questions:
                - Test critical thinking or deeper understanding.
                - Answers should be 150–350 words.

            Output Format:
            - Only return the JSON array. Do not include any explanation, introduction, summary, or extra text.
            - DO not include in value any kind of semi-colon(:) or double-quotes, try to use single quotes i fthere is some sentenc inside value pairs. For example- 
                {{
                    "answer_explanation": "This is called 'Light'"
                }}
            - Do not include characters which could not be parsed as python dictionary data type

            [
                {{
                    "question_number": 1,
                    "question": "",
                    "type_of_question": ["theory",
                        "numerical,
                        "MCQ",
                        "CBQ",
                        "CET",
                        "LO",
                        "Learning Journey",
                        "Activity Based Learning,
                        "Translation"]
                    "options": {{"a": "Option 1", "b": "Option 2", "c": "Option 3", "d": "Option 4"}},  // Include only for Objective
                    "correct_option": "a",  // Leave blank for Subjective
                    "answer_explanation": "",
                    "learning_outcome": "",
                    "answer_word_count": // Should be an integer numer as per the answer count genearted,
                    "difficulty_level": "" // Should be a value from easy, medium or moderate and difficult,
                    "marks": //Integer or float value upto one decimal place 
                }},
            ]

            For hindi subject, below is an example of json response:
            [
                {{
                    "question_number": 1,
                    "question": "यह एक उदाहरण प्रश्न है।",
                    "type_of_question": "MCQ",  
                    "options": {{
                        "a": "विकल्प 1",
                        "b": "विकल्प 2",
                        "c": "विकल्प 3",
                        "d": "विकल्प 4"
                    }},
                    "correct_option": "a",  // Leave blank for Subjective
                    "answer_explanation": "सही उत्तर का कारण।",
                    "learning_outcome": "छात्र कारणों को पहचान सके।",
                    "answer_word_count": 60,
                    "difficulty_level": "medium",
                    "marks": 1
                }}
            ]

        """
        self.learning_objective_prompt = """
            Generate a visually structured set of learning objectives. Follow the D-L-P-T-E approach (Define, Learn, Practice, Test, Evaluate) to ensure comprehensive cognitive coverage. 

            Subject: {subject_name}
            Grade level: {class_name}
            Chapter title: {chapter_name}
            Board: {board_name}
            

            Output Requirements:  
            1. Create 8-10 learning objectives that progress through different cognitive levels
            2. Format each objective using this pattern: "[ACTION VERB] [CONTENT/CONCEPT] [CONTEXT/CONDITION]" 
            3. Begin each objective with an appropriate action verb aligned with the following cognitive categories (Decided on basis of blooms taxonomy): 
            - Lower-order thinking: Remembering and understanding (Define, Identify, List, Describe, Explain) 
            - Mid-order thinking - Application (Apply, Demonstrate, Implement) 
            - Higher-order thinking  - Analyse , Evaluate and Create (Compare, Develop, Differentiate, Evaluate, Assess, Justify, contrast and others from Bloom’s Taxonomy) 
            4. Structure the objectives visually as shown in the reference image:  
            Title: "Learning Objectives" 
            Introduction: "After completing all the chapter sections mapped to the D-L-P-T-E approach, the students will be able to:" 
            - Organize objectives in two columns (5 on left, 5 on right) 
            - Number each objective sequentially  
            - Bold and underline the action verb at the start of each objective. 
            - The learning objectives should create a progression of understanding from basic knowledge to advanced application and evaluation, reflecting a holistic approach to the topic. 
            - Create learning objectives based on the attached PDF and following the instructions listed above.  
            - Create it in a tabular form. 
            - Ensure all the corresponding skills and learning outcomes are taken care form the uploaded file named “Learning skills” 
            - Should be based on the Grade and subject, while creating the learning objectives for the above. 
            - Generate the learning objectives strictly based on the content in the PDF and NOT from any external source.  
            - Include all key concepts from the uploaded PDF. 
            - The language should be grade appropriate
            5. Do not mention the page numbers or any source.
            6. Do not give any examples.
            7. Learning Objectives should be one liner.
            8. Learning Objectives should not be in question format. 
        """

    def chat_api(self, final_prompt):
        try:
            completion = self.client.chat.completions.create(
                # extra_body={},
                # model="qwen/qwq-32b:free",
                model="deepseek/deepseek-r1-distill-llama-70b:free",
                # model="deepseek/deepseek-r1-0528-qwen3-8b:free",
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
            # print("completion-------", completion)
            # Defensive check
            if not completion or not hasattr(completion, "choices") or not completion.choices:
                raise ValueError("No choices returned from model.")

            message = completion.choices[0].message
            if not message or not hasattr(message, "content"):
                raise ValueError("No message content in the first choice.")

            # print("message",message.content)
            return message.content

        except Exception as e:
            print(traceback.format_exc())
            
            print(f"Error in chat_api: {e}")
            return None

    def generate_questions(self, user_prompt, cleaned_data, question_paper_attrs):
        relevant_docs = self.db.similarity_search(user_prompt, k=5)
        retrieved_text = "\n".join([doc.page_content for doc in relevant_docs])
        # final_prompt.format()
        # print(question_paper_attrs, cleaned_data)
        # print(question_paper_attrs['generation_type'])
        # if question_paper_attrs['generation_type'] == "auto":
        #     final_prompt = self.auto_generate_questions_prompt.format(
        #         number_of_questions=15,
        #         number_of_one_mark_questions=settings.DEFAULT_ONE_MARK_QUESTIONS,
        #         number_of_two_mark_questions=settings.DEFAULT_TWO_MARK_QUESTIONS,
        #         number_of_four_mark_questions=settings.DEFAULT_FOUR_MARK_QUESTIONS,
        #         class_name=question_paper_attrs.get('standard_id'),
        #         board_name=question_paper_attrs.get('board_id'),
        #         subject_name=cleaned_data.get('subject_name'),
        #         chapter_name=cleaned_data.get('chapter_name'),
        #         retrieved_text=retrieved_text,
        #         blooms_taxonomy=cleaned_data.get('bloom_filters') or []
        #     )
        # else:
        #     final_prompt = self.prompt.format(
        #         number_of_questions=cleaned_data.get('total_questions') or 15,
        #         subjective_2_marks=cleaned_data.get('subjective_2_marks') or 0,
        #         subjective_4_marks=cleaned_data.get('subjective_4_marks') or 0,
        #         objective_2_options=cleaned_data.get('objective_2_options') or 0,
        #         objective_4_options=cleaned_data.get('objective_4_options') or 0,
        #         case_based=cleaned_data.get('case_based') or 0,
        #         fill_ups=cleaned_data.get('fill_ups') or 0,
        #         match_ups=cleaned_data.get('match_ups') or 0,
        #         language=cleaned_data.get('language') or 'English',
        #         topic=cleaned_data.get('topic') or 'Whole Chapter',
        #         sub_topic=cleaned_data.get('sub_topic') or 'Whole Chapter',
        #         easy_percentage=cleaned_data.get('easy_percentage') or 0,
        #         medium_percentage=cleaned_data.get('medium_percentage') or 0,
        #         difficult_percentage=cleaned_data.get('difficult_percentage') or 0,
        #         very_challenging_percentage=cleaned_data.get('very_challenging_percentage') or 0,
        #         class_name=question_paper_attrs.get('standard_id'),
        #         board_name=question_paper_attrs.get('board_id'),
        #         subject_name=cleaned_data.get('subject_name'),
        #         chapter_name=cleaned_data.get('chapter_name'),
        #         retrieved_text=retrieved_text,
        #         blooms_taxonomy=cleaned_data.get('bloom_filters') or []
        #     )
        service_type_id = cleaned_data.pop('service_type_id', '')
        final_args = {}
        # print("service_type", service_type_id)
        from app.prompt.models import Prompt, SubjectSpecificPrompt, GradeSpecificPrompt
        if service_type_id != 19:
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
                    "match_following": "Match the Following Questions",
                    "critical_analysis": "Critical Analysis Based Questions",
                    "if_based": "If Based Questions",
                }

                question_type_data = {}

                for qtype in QUESTION_TYPE_LABELS.keys():
                    raw_value = cleaned_data.get(qtype)
                    # print("first for", raw_value)
                    if raw_value:
                        try:
                            question_type_data[qtype] = raw_value
                            # print("atd in itry", question_type_data)
                        except Exception as e:
                            # print(f"Warning parsing {qtype}: {e}")
                            question_type_data[qtype] = {}

                # print("qtl-----", question_type_data)
                question_type_lines = []
                
               

                for qtype in QUESTION_TYPE_LABELS.keys():
                    data = question_type_data.get(f"{qtype}", {})
                    # print("in for , data", data)
                    # Load format_args to be used in .format()
                    format_args[f"{qtype}_number_of_questions"] = data.get("number_of_questions", 0)
                    format_args[f"{qtype}_marks_per_question"] = data.get("marks_per_question", 1)
                    format_args[f"{qtype}_total_sub_questions"] = data.get("total_sub_questions", 0)
                    format_args[f"{qtype}_sub_subjective_questions"] = data.get("sub_subjective_questions", 0)
                    format_args[f"{qtype}_sub_objective_questions"] = data.get("sub_objective_questions", 0)
                    num = data.get("number_of_questions", 0)
                    marks = data.get("marks_per_question", 1)
                    total_sub_questions = data.get("total_sub_questions")
                    sub_subjective_questions = data.get("sub_subjective_questions", 0)
                    sub_objective_questions = data.get("sub_objective_questions", 0)
                    print("Number of qustions----------------",num, data.get, sub_subjective_questions)
                    if num > 0:
                        label = QUESTION_TYPE_LABELS.get(qtype, qtype.replace("_", " ").title())
                        # print(label, data.get('number_of_questions'), total_sub_questions)
                        if data.get('number_of_questions'):
                            if total_sub_questions:
                                question_type_lines.append(f"- {num} {label}, each carrying {marks} mark(s) with {total_sub_questions} sub-questions each, ({sub_subjective_questions} Subjective, {sub_objective_questions} Objective)")
                            else:
                                question_type_lines.append(f"- {num} {label}, each carrying {marks} mark(s)")
                            
                # print("format-args", format_args)


                # Create final string block to inject into the prompt
                final_args["question_type_block"] = "\n".join(question_type_lines) if question_type_lines else "No questions specified."
                # print("dinal format lines", format_args)
            else:
                # print("in else")
                cleaned_data['total_questions'] = 5
                final_args["question_type_block"] = """- 1 Mulitple Choice Questions, each carrying 1 mark
                    - 1 Fill in the blanks, each carrying 1 mark,
                    - 1 Short Answer Questions with word limit upto 200 each carrying 3 marks,
                    - 2 Long Answer Questions with word limit upto 500 each carrying 4 marks
                    - No any other question type like Statement Based, case Based, Assertion Reason, Paragraph based, Source Based, etc to be framed apart from mentioned above
                """

        if service_prompt := Prompt.objects.get_by_service_type_id(service_type_id):
            # print("desc---------->", service_prompt.description)
            
            final_prompt = service_prompt.description.format(
                total_questions=cleaned_data.get('total_questions'),
                class_name=cleaned_data.get('standard_id'),
                board_name=cleaned_data.get('board_id'),
                subject_name=cleaned_data.get('subject_name'),
                chapter_name=cleaned_data.get('chapter_name'),
                number_of_lo=cleaned_data.get('number_of_lo') or 8-10,
                topic=cleaned_data.get('topic'),
                sub_topic=cleaned_data.get('sub_topic'),
                easy_percentage=cleaned_data.get('easy_percentage', 30),
                medium_percentage=cleaned_data.get('medium_percentage', 30),
                difficult_percentage=cleaned_data.get('difficult_percentage', 30),
                very_challenging_percentage=cleaned_data.get('very_challenging_percentage', 10),
                **final_args
            )
            if subject_prompt := SubjectSpecificPrompt.objects.get_by_prompt_and_subject_id(service_prompt, cleaned_data.get('subject_id')):
                final_prompt = final_prompt.replace("__SUBJECT_SPECIFIC_GUIDELINES__", subject_prompt.description)
            if grade_prompt := GradeSpecificPrompt.objects.get_by_prompt_and_grade_id(service_prompt, cleaned_data.get('standard_id')):
                final_prompt = final_prompt.replace("__GRADE_SPECIFIC_GUIDELIENS__", grade_prompt.description)
            # print(final_prompt)
            fp = Helper.generate_final_prompt(service_prompt.service_type.service_type, cleaned_data.get('standard_id'), cleaned_data.get('subject_name'), final_prompt)
            # print("final---------", fp)
            # print(cleaned_data.get('language').lower(), cleaned_data.get('language').lower() == 'english')
            if not cleaned_data.get('language').lower() == 'english':
                fp += f"\n Please generate output in {cleaned_data.get('language')} strictly."
            else:
                fp += f"\n Please generate output in Academic British English."
            print("***************************", fp)
            # print(abc)
            return self.chat_api(fp)
            # return {}
