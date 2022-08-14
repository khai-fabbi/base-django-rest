from typing import Any, Dict

from django.utils import timezone
from rest_framework.renderers import JSONRenderer as OriginalJSONRenderer


class JSONRenderer(OriginalJSONRenderer):
    """Custom JSONRenderer"""

    def render(self, data, accepted_media_type=None, renderer_context=None):
        ret: Dict[str, Any] = {
            'status': 'OK',
            'data': None,
            'error': None,
            'time': timezone.now()
        }

        if data is not None:
            if 'error' in data:
                ret['status'] = 'ERROR'
                ret['error'] = data.get('error')
            else:
                ret['data'] = data

        return super().render(ret, accepted_media_type, renderer_context)
