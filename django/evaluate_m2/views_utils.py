
from django.conf import settings
from django.contrib.auth.models import User

def has_permissions_for_request(request, event) -> bool:
    if settings.SSO_ENABLED:
        user = User.objects.get(username=request.user.username)
        return event.check_access_for_user(user)
    else:
        return True

def get_randomizer(result_total, total_per_page) -> int:
    randomizer = 1
    if result_total > total_per_page:
        randomizer = result_total // total_per_page
    return randomizer