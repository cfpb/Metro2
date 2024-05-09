
from django.conf import settings
from django.contrib.auth.models import User

def has_permissions_for_request(request, event) -> bool:
    if hasattr(settings, 'ENABLE_SSO') and settings.ENABLE_SSO.lower() == "enabled":
        user = User.objects.get(username=request.user.username)
        return event.check_access_for_user(user)
    return True
