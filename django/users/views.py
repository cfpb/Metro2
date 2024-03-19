import logging

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, JsonResponse
from django.shortcuts import render

from users.exception_utils import get_users_not_found_exception
from users.models import Dataset
from users.serializers import UserViewSerializer

def unsecured_view(request):
    return render(request, "m2/page.html")


@login_required
def secured_view(request):
    return render(request, "m2/page.html")


@login_required
def datasets(request):
    datasets = Dataset.objects.filter(
        user_group__in=request.user.groups.all()
    )
    context = { "datasets": datasets }
    return render(request, "m2/datasets.html", context)

@login_required
def dataset(request, dataset_id):
    dataset = Dataset.objects.get(id=dataset_id)
    if not dataset.check_access_for_user(request.user):
        msg = "Dataset does not exist or you do not have permission to view it."
        raise Http404(msg)

    context = { "dataset": dataset }
    return render(request, "m2/dataset.html", context)

@api_view(('GET',))
def users_view(request, user_id=0):
    logger = logging.getLogger('views.user_view')
    try:
        # username is retrieved from the request if SSO is enabled
        # user_id from the URL will be used if SSO is not enabled
        user = User.objects.get(username=request.user.username) \
                if user_id == 0 \
                else User.objects.get(id=user_id)
        userSerializer = UserViewSerializer(user)
        return JsonResponse(userSerializer.data)
    except User.DoesNotExist:
        error = get_users_not_found_exception(user_id, request.path)
        logger.error(error['message'])
        return Response(error, status=status.HTTP_404_NOT_FOUND)
