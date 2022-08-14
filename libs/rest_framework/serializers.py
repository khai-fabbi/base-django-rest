from rest_framework.exceptions import ValidationError

from helpers.exceptions import BadRequest, get_first_error_detail


class OnlyOneErrorMixin:
    def is_valid(self, raise_exception=False):
        # This implementation is the same as the default,
        # except that we use lists, rather than dicts, as the empty case.
        assert hasattr(self, 'initial_data'), (
            'Cannot call `.is_valid()` as no `data=` keyword argument was '
            'passed when instantiating the serializer instance.'
        )

        if not hasattr(self, '_validated_data'):
            try:
                self._validated_data = self.run_validation(self.initial_data)
            except ValidationError as exc:
                self._validated_data = []
                self._errors = exc.detail
            else:
                self._errors = []

        if self._errors and raise_exception:
            try:
                first_error = get_first_error_detail(self.errors)
            except Exception:
                raise ValidationError(self.errors)
            else:
                raise BadRequest(detail=first_error, code=getattr(first_error, 'code', 'invalid'))

        return not bool(self._errors)
