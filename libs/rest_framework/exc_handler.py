import re
from typing import Any, Optional

from django.utils.translation import gettext_lazy
from rest_framework.exceptions import ErrorDetail
from rest_framework.response import Response
from rest_framework.views import exception_handler

from helpers.exceptions import InternalServerError, get_first_error_detail


def custom_exception_handler(exc: Exception, context: Any) -> Optional[Response]:
    """Handle all APIExceptions occured after receiving HTTP request.

    Args:
        exc (Exception): Exception.
        context (Any): Exception context.

    Returns:
        Optional[Response]: HTTP error response.
    """

    # Call rest_framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        code = InternalServerError.default_code
        detail = InternalServerError.default_detail
        status_code = InternalServerError.status_code

        if hasattr(exc, 'detail'):
            status_code = exc.status_code
            code = getattr(exc.detail, 'code', None) or getattr(exc, 'default_code', None)

            detail = getattr(exc, 'detail', '')

            if not isinstance(detail, ErrorDetail):
                try:
                    detail = get_first_error_detail(detail)
                except Exception:
                    pass

            detail = str(detail)
            params = re.findall(r'\`(.*?)\`', detail)

            if len(params):
                detail = re.sub(r'\`(.*?)\`', '`%s`', detail)
                message = gettext_lazy(detail) % tuple(params)
            else:
                message = gettext_lazy(detail)

        response.data = {
            'status': 'ERROR',
            'error': {
                'code': code,
                'message': message,
            }
        }
        response.status_code = status_code
        response.content_type = 'application/json'

    return response
