from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def unsecured_view(request):
    return render(request, "m2/page.html")


@login_required
def secured_view(request):
    return render(request, "m2/page.html")