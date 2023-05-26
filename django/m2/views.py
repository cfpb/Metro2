from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from m2.models import Dataset


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
def dataset(request, dataset_name):
    # TODO: ensure user has this dataset permission before serving
    info = Dataset.objects.get(name=dataset_name)
    context = { "dataset": info }
    return render(request, "m2/dataset.html", context)