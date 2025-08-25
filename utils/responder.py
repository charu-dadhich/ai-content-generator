from django.http.response import JsonResponse
from .constants import Constant


class Responder():

    @classmethod
    def send(cls, code, data, status=True, http_code=200):
        message = Constant.responder_messages[code]
        print(JsonResponse({'code': code, 'message': message, 'status': status, 'data': {}}, status=http_code))
        return JsonResponse({'code': code, 'message': message, 'status': status, 'data': data}, status=http_code)
    
    @classmethod
    def error(cls, code, error, status=False, http_code=400):
        message = Constant.responder_messages[code]
        print(JsonResponse({'code': code, 'message': message, 'status': status, 'error': error}, status=http_code))
        return JsonResponse({'code': code, 'message': message, 'status': status, 'error': error}, status=http_code)
