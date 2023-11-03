from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render

from users.models import Dataset


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
