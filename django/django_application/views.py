from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view()
def bad_request_view(request):
    return Response(status=status.HTTP_400_BAD_REQUEST)
