import traceback
from django.utils import timezone
from utils import Logger


class LoggerMiddleware():
    def __init__(self, get_response):
        self.start_time = 0
        self.get_response = get_response

    def __call__(self, request):
        self.start_time = timezone.localtime()
        content_type = request.META.get('CONTENT_TYPE', '')
        print("content------", content_type, request.method)
        request.extracted_body = {}
        if content_type.startswith("application/json"):
            try:
                request.extracted_body = request.body.decode("utf-8", errors="replace")
                print("JSON Body:", request.extracted_body)
            except Exception as e:
                print(f"Error reading JSON body: {e}")
                request.extracted_body = ""

        elif content_type.startswith("multipart/form-data"):
            print("Form fields:")
            request.extracted_body = {}
            for key, value in request.POST.items():
                # print(f"{key} = {value}")
                request.extracted_body[key] = value
                print(type(value))

            print("Uploaded files:")
            for key, file in request.FILES.items():
                print(f"{key}: name={file.name}, size={file.size}, content_type={file.content_type}")
                request.extracted_body['file_name'] = file.name
                request.extracted_body['file_size'] = file.size
                request.extracted_body['content_type'] = file.content_type
        print("body extracted from request", request.extracted_body)
        response = self.get_response(request)
        # print("after view respomse")
        Logger.info(request, response, self.start_time)
        return response
    
    def process_view(self, request, view, view_args, view_kwargs):
        return None

    # def process_view(self, request, *args, **kwargs):
    #     if hasattr(request, '_body'):
    #         # Body cached, safe to access
    #         body_bytes = request._body
    #         print("inside has attribute _body", body_bytes)
    #     else:
    #         if getattr(request, '_read_started', False):
    #             print("2")
    #             # Stream partially read, unsafe to access body
    #             # Skip reading body or handle gracefully
    #             body_bytes = None
    #         else:
    #             print("3")
    #             # Stream not read yet, safe to read and cache body
    #             body_bytes = request.body  # This reads and caches _body internally

    #     # Now you can decode or log body_bytes if not None
    #     if body_bytes:
    #         body_text = body_bytes.decode('utf-8', errors='ignore')
    #         print("Request body:", body_text)

    
    def process_exception(self, request, exception):
        print("inside exception from view", request)
        detail = traceback.format_exc()
        Logger.error(request, exception, detail)
        return None
    
    def process_template_response(self, request, response):
        # print("inside process template", response, request)
    # if hasattr(response, 'data') and response.data.get('code', 500) != 500:
        # print(f"Response class: {response.__class__.__name__}")
        return response
