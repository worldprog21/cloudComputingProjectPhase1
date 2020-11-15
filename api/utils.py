from rest_framework.pagination import PageNumberPagination

class CategoryPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'size'


def custom_exception_handler(exc, context):
    from rest_framework.views import exception_handler
    from rest_framework.response import Response
    from pprint import pprint
    from django.http.response import Http404

    response = exception_handler(exc, context)

    if hasattr(exc, 'detail'):
        detail = exc.detail
    elif response and hasattr(response, 'data') and 'detail' in response.data:
        detail = str(response.data['detail'])
    else:
        detail = str(exc)

    if hasattr(exc, 'get_codes'):
        code = exc.get_codes()
    elif response and response.data and hasattr(response.data['detail'], 'code'):
        code = response.data['detail'].code
    else:
        code = None

    if hasattr(response, 'status_code'):
        status_code = response.status_code
    else:
        status_code = 406
    
    return Response({
        "message"       : detail,
        "code"          : code,
        "status_code"   : status_code
    }, status=status_code)
