from django.conf import settings
from django.contrib.auth.models import User

from django_application.s3_utils import s3_resource

def has_permissions_for_request(request, event) -> bool:
    if settings.SSO_ENABLED:
        user = User.objects.get(username=request.user.username)
        return event.check_access_for_user(user)
    else:
        return True

def get_s3_bucket():
    bucket = s3_resource()
    return bucket
