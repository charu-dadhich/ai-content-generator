from django.http.response import JsonResponse
from rest_framework.response import Response
from question_ai.exception import ApiException
from .constants import Constant


class Responder:

    @staticmethod
    def _data(data, count):
        if count is None:
            return data or {}
        return {"results": data or [], "count": count}

    @staticmethod
    def _build_response(code, data, count, status, http_status_code, error, message):
        response_data = {
            "status": status,
            "code": code,
            "message": message or Constant.response_messages[code],
            "data": Responder._data(data, count),
        }
        if error:
            response_data["error"] = error
        return Response(response_data, status=http_status_code)

    @classmethod
    def send(cls, code, data=None, count=None, status=True, http_status_code=200, error=None, message=None):
        return cls._build_response(code, data, count, status, http_status_code, error, message)

    @staticmethod
    def throw_error(code, http_status_code=400, status=False):
        raise ApiException(code, http_status_code, status)

    @classmethod
    def accept(cls, code, http_status_code=202, status=True):
        raise ApiException(code, http_status_code, status)
