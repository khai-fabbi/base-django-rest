import logging

from django.conf import settings
from django.db import connection
from django.http import JsonResponse, QueryDict
from django.utils import translation
from rest_framework.exceptions import APIException

from helpers.exceptions import InternalServerError
from helpers.utils import get_request_ip

logger = logging.getLogger(__name__)


class HandleExceptionMiddleware(object):
    """
    Middleware này được sử dụng cho mục đích xử lý các exception mà không phải là subclass của class rest_framework.exceptions.APIException.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if not isinstance(exception, APIException):  # pragma: no branch
            logger.exception(exception)

            return JsonResponse(data={
                'code': InternalServerError.default_code,
                'message': InternalServerError.default_detail
            }, status=InternalServerError.status_code)


class PreProcessingMiddleware(object):
    """
    Middleware này được sử dụng cho mục đích chặn bắt ngay khi request đến và thiết lập các giá trị cần thiết ban đầu.
    Lấy giá trị language và IP address sau đó đưa vào thuộc tính của object request.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            request.META['HTTP_ACCEPT_LANGUAGE'] = settings.LANGUAGE_CODE

        query_dict = QueryDict(request.META['QUERY_STRING'])

        language = query_dict.get('language')
        language = language if language is not None else settings.LANGUAGE_CODE

        supported_languages = settings.SUPPORTED_LANGUAGES

        if language in supported_languages:
            request.language = language

            if language != translation.get_language():
                translation.activate(language)

        request.ip = get_request_ip(request)

        response = self.get_response(request)

        return response


class QueryCountDebugMiddleware(object):  # pragma: no cover
    """Debug query count - use for DEBUG only."""
    """
    This middleware will log the number of queries run
    and the total time taken for each request (with a
    status code of 200). It does not currently support
    multi-db setups.
    """

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if settings.DEBUG:
            total_time = 0

            for query in connection.queries:
                query_time = query.get('time')
                print(f'{self.WARNING}------------------------------------{self.ENDC}')
                print(f'{self.FAIL}=== SQL === {self.OKBLUE}' + str(query) + self.ENDC)

                if query_time is None:
                    query_time = query.get('duration', 0) / 1000
                total_time += float(query_time)

            print(f'{self.OKGREEN}==== CONCLUSSION ===> %s queries run, total %s seconds' % (len(connection.queries), total_time) + self.ENDC)

        return response
