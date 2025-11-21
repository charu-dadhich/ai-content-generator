from loguru import logger
from django.conf import settings
from django.utils import timezone


class Logger:
    logger.remove()
    base_path  = f'{settings.BASE_DIR}/logs/{{time:YYYY}}/{{time:MMMM}}/{{time:DD}}'
    loggers = {}

    def _log_filter(filename):
        def filter(record):
            return record['extra'].get('filename') == filename
        return filter

    for filename in ['server', 'error']:
        loggers[filename] = logger.bind(filename=filename)
        loggers[filename].add(
            f'{base_path}/{filename}.log',
            rotation='00:00',
            enqueue=True,
            level='DEBUG',
            format='{message}',
            filter=_log_filter(filename)
        )

    @classmethod
    def info(cls, request, response, start_time):
        request_body = getattr(request, 'extracted_body', 'NA')
        # print("inside logger file", request_body)
        current_time = timezone.localtime().strftime("%I:%M:%S %p (%Z)")
        headers_duplicate = dict(request.headers)
        execution_time = (timezone.localtime() - start_time).total_seconds()
        # print(execution_time, request_body, request, headers_duplicate)
        data = f'''
            {current_time} | IP [{request.META.get('REMOTE_ADDR')}]
            {request.build_absolute_uri()} ({request.method})
            REQUEST_HEADERS {headers_duplicate}
            REQUEST_BODY {request_body}
            RESPONSE_HEADERS {response.headers}
            STATUS_CODE ~ {response.status_code} | EXECUTION_TIME [{execution_time} Seconds]
            *************************************************************\n'''     # noqa
        data = data.replace('  ', '')
        # print("data----------->", data)
        cls.loggers['server'].info(data.replace('  ', ''))

    @classmethod
    def error(cls, request, error):
        request.data.pop('file_content', '')
        data = f'''XXXXXXXXXXXXXXXXXXXXXXXXXX[ ERROR ]XXXXXXXXXXXXXXXXXXXXXXXXXX
        Unable to process the request: {request}
        Request data: {request.data}
        Error: {error}
        *************************************************************\n'''.replace('  ', '')
        cls.loggers['error'].error(data)
