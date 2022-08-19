from rest_framework.exceptions import APIException
from rest_framework import status
class CategoryExeption(APIException):
    status_code = 400
    default_detail = "Unable to read file."
    default_code = "unreadable_csv_file"

class PageNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = '見つかりません'
    default_code = 'not_found'