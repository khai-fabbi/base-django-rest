import logging

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException, ErrorDetail

logger = logging.getLogger(__name__)


def get_first_error_detail(errors, detail=None, depth=0) -> ErrorDetail:
    if depth >= 8:
        return ErrorDetail('Depth: Too many levels.', code='too_many_levels')

    if isinstance(errors, dict):
        errors = list(errors.values())

    if isinstance(errors, list):
        for error in errors:
            if error:
                if isinstance(error, (list, dict)):
                    detail = get_first_error_detail(error, detail, depth + 1)
                else:
                    detail = error

                return detail if isinstance(detail, ErrorDetail) else ErrorDetail(str(detail), code='invalid')


class InternalServerError(APIException):
    """
    Exception được trả về khi có lỗi nhưng chưa rõ nguyên nhân.
    """

    default_code = 'internal_server_error'
    default_detail = _('Internal server error')


class BadRequest(APIException):
    """
    Exception được trả về khi có lỗi do request data.
    """
    default_code = 'bad_request'
    default_detail = _('Bad Request')
    status_code = status.HTTP_400_BAD_REQUEST
