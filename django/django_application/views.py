from django.conf import settings

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view()
@permission_classes([IsAuthenticated])
def version(request):
    return Response({"version": settings.VERSION})


@api_view()
def bad_request_view(request):
    return Response(status=status.HTTP_400_BAD_REQUEST)
