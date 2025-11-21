import traceback
from rest_framework.decorators import api_view
from django.conf import settings
from django.http import JsonResponse
from django.urls.exceptions import Resolver404
from rest_framework.exceptions import (
    MethodNotAllowed,
    ParseError,
    UnsupportedMediaType,
    NotAuthenticated,
    AuthenticationFailed,
    PermissionDenied,
    ValidationError as DRFValidationError,
    Throttled,
)

from .exception import ApiException
from utils import (
    Responder,
    Logger,
)


def handle_errors(exception, context):
    error_mappings = {
        ApiException: lambda ex: handle_api_exception(ex),
        MethodNotAllowed: 505,
        Resolver404: 501,
        ParseError: 502,
        PermissionDenied: 506,
        Throttled: 510,
        UnsupportedMediaType: 503,
        NotAuthenticated: 504,
        AuthenticationFailed: 504,
        DRFValidationError: lambda ex: handle_validation_error(ex),
    }
    response_code = error_mappings.get(type(exception), 500)
    http_status_code = getattr(exception, 'status_code', 500)
    if callable(response_code):
        response_code = response_code(exception)
    if isinstance(response_code, dict) and (
        response_code["response_code"] == 507 or response_code["response_code"] == 508
    ):
        return Responder.send(response_code["response_code"], error=response_code["data"], status=False, http_status_code=400)
    if response_code == 500:
        http_status_code = 500
        Logger.error(context.get("request"), traceback.format_exc())
        if settings.DEBUG:
            raise exception
    return Responder.send(response_code, status=False, http_status_code=http_status_code)


def handle_api_exception(exception):
    return exception.error_code


def unpacking_error(error_details):
    data = {}
    if isinstance(error_details, dict):
        for key, val in error_details.items():
            if isinstance(val, dict):
                data[key] = unpacking_error(val)
            if isinstance(val, list):
                data[key] = str(val[0])
    if isinstance(error_details, list):
        # If it's a list, just extract the string error message from the first item
        data = str(error_details[0])
    return data


def handle_validation_error(exception):
    error_details = exception.detail
    response_code = 507
    data = unpacking_error(error_details)
    return {
                "response_code": response_code,
                "data": data
            }


def custom_404_view(request, exception=None):
    return JsonResponse(
        {"status": "Failed", "message": "The requested resource was not found"},
        status=404
    )
