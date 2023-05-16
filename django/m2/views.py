from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse



temp = """
<html> <body> <h1>Testing</h1> {} </body> </html>
"""



def unsecured_view(request):
    return HttpResponse(temp.format("<p>This is the unsecured view<p>"))


@login_required
def secured_view(request):
    u: User = request.user
    msg = f"<p>This view is secured</p><p>you are logged in as {u.username}</p>"
    return HttpResponse(temp.format(msg))