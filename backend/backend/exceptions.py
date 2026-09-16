from rest_framework import status
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return response

    detail = response.data
    if isinstance(detail, dict) and 'detail' in detail:
        message = detail['detail']
    else:
        message = detail

    response.data = {
        'code': response.status_code,
        'message': message,
        'data': None,
    }
    if response.status_code == status.HTTP_401_UNAUTHORIZED:
        response.data['code'] = 401
    return response
