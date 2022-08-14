from django.utils.translation import gettext_noop as _
from rest_framework import fields
from rest_framework.exceptions import ValidationError


class CustomField():
    default_error_messages = {
        'required': _('This field `%s` is required.'),
        'null': _('This field `%s` may not be null.'),
        'invalid': _('Value of field `%s` is invalid.'),
        'blank': _('This field `%s` may not be blank.'),
        'invalid_choice': _('Value of field `%s` is invalid.'),
    }

    def fail(self, key, **kwargs):
        try:
            msg = self.error_messages[key]
        except KeyError:
            class_name = self.__class__.__name__
            msg = fields.MISSING_ERROR_MESSAGE.format(class_name=class_name, key=key)
            raise AssertionError(msg)

        message_string = msg.format(**kwargs)
        try:
            # place this in try/except for case: custom error messages not include `%s`.
            message_string = message_string % self.field_name
        except Exception:
            pass

        raise ValidationError(message_string, code=key)


class CharField(CustomField, fields.CharField):
    pass


class BooleanField(CustomField, fields.BooleanField):
    pass


class IntegerField(CustomField, fields.IntegerField):
    pass


class ChoiceField(CustomField, fields.ChoiceField):
    pass
