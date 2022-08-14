import re
from typing import Any, Dict, Union

from django.http.request import HttpRequest


def get_request_ip(request: HttpRequest) -> str:
    """Get IP address of HTTP request.

    Args:
        request (HttpRequest): HTTP request

    Returns:
        str: IP address v4.
    """

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

    return ip


def camel_to_snake(obj: Union[Dict[str, Any], str]
                   ) -> Union[Dict[str, Any], str]:
    """Convert key của dict hoặc một chuỗi string từ camelCase thành snake_case

    Args:
        obj (Union[Dict[str, Any], str]): Input với type là string hoặc dictionary.

    Returns:
        Union[Dict[str, Any], str]: Output.
    """

    if isinstance(obj, Dict):
        new_dict: Dict[str, Any] = {}

        for key, value in obj.items():
            new_key = str(camel_to_snake(key))
            new_dict[new_key] = value

        return new_dict
    else:
        pattern = re.compile(r'(?<!^)(?=[A-Z])')
        return pattern.sub('_', obj).lower()
