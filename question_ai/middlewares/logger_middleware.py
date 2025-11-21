import traceback
from django.utils import timezone
from utils import Logger


class LoggerMiddleware():
    def __init__(self, get_response):
        self.start_time = 0
        self.get_response = get_response

    def __call__(self, request):
        self.start_time = timezone.localtime()
        request.extracted_body = {}
        content_type = request.META.get('CONTENT_TYPE', '')
        if content_type.startswith("application/json"):
            try:
                request.extracted_body = request.body.decode("utf-8", errors="replace")
            except Exception as e:
                print(f"Error reading JSON body: {e}")
                request.extracted_body = ""

        elif content_type.startswith("multipart/form-data"):
            request.extracted_body = {}
            for key, value in request.POST.items():
                request.extracted_body[key] = value
            for key, file in request.FILES.items():
                request.extracted_body['file_name'] = file.name
                request.extracted_body['file_size'] = file.size
                request.extracted_body['content_type'] = file.content_type
        response = self.get_response(request)
        Logger.info(request, response, self.start_time)
        return response
    
    def process_view(self, request, view, view_args, view_kwargs):
        return None
    
    def process_exception(self, request, exception):
        detail = traceback.format_exc()
        Logger.error(request, exception)
        return None
    
    def process_template_response(self, request, response):
        if hasattr(response, 'data') and response.data.get('code', 500) != 500:
            Logger.info(request, response, self.start_time)
        return response
