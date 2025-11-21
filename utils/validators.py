import re
import demjson3
from .responder import Responder


class Validator:

    @classmethod
    def validate_password(cls, password, old_password=None):
        if old_password and old_password == password:
            Responder.accept(105)
        if len(password) < 8:
            Responder.accept(107)
        if not re.findall(r"\d", password):
            Responder.accept(108)
        if not re.findall(r"[A-Z]", password):
            Responder.accept(109)
        if not re.findall(r"[a-z]", password):
            Responder.accept(110)
        if not re.findall(r"[ ()[\]{}|\\`~!@#$%^&*_\-+=;:\"',<>./?]", password):
            Responder.accept(111)

    @classmethod
    def extract_json_from_ai_response(cls, ans):
        cleaned_text = re.sub(r"```json\s*([\s\S]*?)```", r"\1", ans, flags=re.MULTILINE)
        cleaned_text = cleaned_text.strip('` \n\r\t')
        try:
            parsed = demjson3.decode(cleaned_text)
            if isinstance(parsed, list):
                return parsed
            else:
                return parsed
        except Exception as e:
            return None
