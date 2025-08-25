from utils.constants import Constant


class Helper:

    WORKSHEETS_SUBJECT_CONDITIONAL_SNIPPETS = {
        "hindi": """
            Hindi-Specific Guidelines:
            - Use simple, everyday Hindi
            - Avoid Sanskrit-heavy words
            - Stick to NCERT-style explanations
            - Provide Entire Output in Hindi. 
            - Use the rules of मानक हिन्दी (Academic) in terms of punctuation marks and the spellings.  
        """,
        "mathematics": """
            Math-Specific Guidelines:
            - Focus on step-by-step solutions
            - Use clear notation and formatting
            - Avoid real-life word problems unless specified
            - Make sure you make no calculation errors, and all the question solved are conceptually sound and mathematically consistent. 
        """,
        "science": """
            Science-Specific Guidelines:
            - Include real-world analogies
            - Keep technical terms age-appropriate
            - Include numericals as well, wherever possible in chapter
        """,
        "chemistry": """
            Science-Specific Guidelines:
            - Include real-world analogies
            - Keep technical terms age-appropriate
            - Include numericals as well, wherever possible in chapter
        """,
        "physics": """
            Science-Specific Guidelines:
            - Include real-world analogies
            - Keep technical terms age-appropriate
            - Include numericals as well, wherever possible in chapter
        """,
        "biology": """
            Science-Specific Guidelines:
            - Include real-world analogies
            - Keep technical terms age-appropriate
            - Include numericals as well, wherever possible in chapter
        """
    }

    LEARNING_OBJECTIVES_CONDITIONAL_STATEMENTS = {

    }

    K5_WORKSHEETS_GRADE_CONDITIONAL_SNIPPETS = {
        "K5":
        """
            Use Indian contexts in the questions. Use contexts from villages, towns, cities, different metro cities and non-metro cities. The correct answer should be explicitly correct, but the other options also should not be too obviously incorrect. Child has to think before choosing any option as correct option. \n
            Interdisciplinary Questions to be added from the grade appropriate. \n
        """
    }

    K12_WORKSHEETS_GRADE_CONDITIONAL_SNIPPETS= """
        ⚠️ Very Important Instructions:

        1. At least **50% of the Short and Long Answer Questions must be numerical**. These should involve step-by-step calculations using formulas

        2. **Do not create simple plug-and-play numericals** (like "F = 20, a = 2, find m"). These are low-rigor. Instead, embed the numericals into **real-life scenarios** and require **multi-step reasoning**.

        3. Use **real-world contexts**, but ensure the problem:
        - Requires use of appropriate formulas
        - Involves 2–3 steps to solve
        - Includes units and correct SI usage

        4. Increase cognitive load by:
        - Requiring conversions
        - Asking for interpretation of the result
        - Including reasoning about force directions or interactions

        5. For Short/Long Answers, your output must include:
        - Step-by-step answer explanation
        - Correct units
        - Final boxed answer (if needed)
    """

    @classmethod
    def generate_final_prompt(cls, service_type_name, class_name, subject_name, base_prompt):
        if class_name >= 1 and class_name <=5:
            class_name = 'K5'
        elif class_name >=9 and class_name <= 12:
            class_name = 'K12'
        print("name of my service", class_name)
        grade_conditional_service_prompt = ''
        #     print("in if for class", class_name)
        # print(class_name, service_type_name.upper())
        # sub_conditional_service_prompt = getattr(cls, f"{service_type_name.upper()}_SUBJECT_CONDITIONAL_SNIPPETS", {})
        # grade_conditional_service_prompt = getattr(cls, f"{class_name}_{service_type_name.upper()}_GRADE_CONDITIONAL_SNIPPETS", {})
        # print("grade_conditional_service_prompt", grade_conditional_service_prompt)
        if service_type_name.upper() != "LEARNING OBJECTIVES":
            # print("i am in general rule for qt in lo")
            general_question_type_rule = Constant.GENERAL_QUESTIONS_FORMAT
            # print(type(base_prompt), "type of base prompt")
            base_prompt = base_prompt.replace("__GENERAL_QUESTIONS_FORMAT__", general_question_type_rule)
            # print("base prompt, in helper", base_prompt)
        # subject_specific_prompt = sub_conditional_service_prompt.get(subject_name.lower(), "")
        # class_specific_prompt = grade_conditional_service_prompt
        # print(class_specific_prompt)
        final_prompt = base_prompt 
        # print(abc)
        print("finallllll-------------", final_prompt)
        # print(diejij)
        return final_prompt
