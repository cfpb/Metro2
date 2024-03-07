import logging
import json
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

from users.models import Dataset
from users.serializers import GroupSerializer

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

api_view()
def users_view(request, user_id):
    logger = logging.getLogger('views.user_view')
    try:
        groups = []
        response = {}
        user = User.objects.get(id=user_id)
        groupSerializer = GroupSerializer(user.groups.all(), many=True)
        groups = json.dumps(groupSerializer.data)
        response = {
            "is_admin": True if user.is_superuser == 1 else False,
            "username": user.username,
            "assigned_events": json.loads(groups)
        }
        return JsonResponse(response)
    except User.DoesNotExist as e:
        logger.error(e)
        return Response(e, status=status.HTTP_404_NOT_FOUND)
