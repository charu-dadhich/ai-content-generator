import os
import jwt
import base64
import PyPDF2
import time
import random
from django.utils.timezone import now, timedelta
from django.conf import settings
from .constants import Constant
from .responder import Responder
from .logger import Logger


class Helper:

    jwt_secret_key = settings.SECRET_KEY
    auth_token_expiry_days = settings.AUTH_TOKEN_EXPIRY_DAYS

    @classmethod
    def generate_final_prompt(cls, service_type_name, class_name, subject_name, base_prompt):
        if class_name >= 1 and class_name <= 5:
            class_name = 'K5'
        elif class_name >= 9 and class_name <= 12:
            class_name = 'K12'
        if service_type_name.upper() != "LEARNING OBJECTIVES":
            general_question_type_rule = Constant.GENERAL_QUESTIONS_FORMAT
            base_prompt = base_prompt.replace("__GENERAL_QUESTIONS_FORMAT__", general_question_type_rule)
        final_prompt = base_prompt
        return final_prompt

    @classmethod
    def check_can_generate(cls, last_generation_time):
        current_time = now()
        print(last_generation_time)
        time_difference_in_seconds = (current_time - last_generation_time).total_seconds()
        print("time", time_difference_in_seconds)
        if time_difference_in_seconds > settings.GENERATION_TIME_IN_SECONDS:
            return True
        return False

    @classmethod
    def encode_jwt(cls, payload, current_time):
        timeout = timedelta(days=cls.auth_token_expiry_days)
        expiry_time = current_time + timeout
        payload.update({
            "exp": expiry_time,
            "iat": current_time,
        })
        return jwt.encode(payload, cls.jwt_secret_key, algorithm="HS256")

    @classmethod
    def decode_jwt(cls, token, code=509):
        try:
            return jwt.decode(
                token, cls.jwt_secret_key, algorithms=["HS256"]
            )
        except Exception as e:
            print(e)
            Responder.throw_error(code)

    @classmethod
    def decode_file_content(cls, encoded_str):
        decoded_bytes = base64.b64decode(encoded_str)
        seconds_since_epoch = int(time.time())
        random_number = random.randint(10000, 99999)
        output_file = f"output-{seconds_since_epoch}-{random_number}.pdf"
        with open(output_file, 'wb') as pdf_file:
            pdf_file.write(decoded_bytes)
        with open(output_file, 'rb') as file:
            try:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
            except Exception as e:
                # Logger.error(request, e)
                Responder.accept(194)
        os.remove(output_file)
        return text
