import logging
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from django.http import JsonResponse

from users.exception_utils import get_users_not_found_exception
from users.serializers import UserViewSerializer


@api_view(('GET',))
def users_view(request, user_id=0):
    logger = logging.getLogger('views.user_view')
    try:
        ENABLE_SSO = os.environ.get('ENABLE_SSO')
        user=None
        # username is retrieved from the request if SSO is enabled
        # user_id from the URL will be used if SSO is not enabled or
        # if the user_id is not provided, use 1
        if ENABLE_SSO and ENABLE_SSO.lower() == "enabled":
            user = User.objects.get(username=request.user.username)
        else:
            if user_id == 0:
                user = User.objects.get(id=1)
            else:
                user = User.objects.get(id=user_id)

        userSerializer = UserViewSerializer(user)
        return JsonResponse(userSerializer.data)
    except User.DoesNotExist:
        error = get_users_not_found_exception(user_id, request.path)
        logger.error(error['message'])
        return Response(error, status=status.HTTP_404_NOT_FOUND)
