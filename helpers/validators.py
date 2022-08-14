from datetime import datetime

from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from helpers.constants import DATETIME_FORMAT


class DateTimeValidator:
    """Validator for validating values in datetime format."""

    format = DATETIME_FORMAT

    def __init__(self, format=None):
        if format is not None:
            self.format = format

    def __call__(self, value):
        try:
            datetime.strptime(value, self.format)
        except Exception:
            raise ValidationError(_('Invalid datetime format.'))
