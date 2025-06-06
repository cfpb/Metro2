import logging

from django.conf import settings
from django.contrib.auth.models import User

from parse_m2.models import Metro2Event

def has_permissions_for_request(request, event: Metro2Event) -> bool:
    if settings.SSO_ENABLED:
        user = User.objects.get(username=request.user.username)
        return event.check_access_for_user(user)
    else:
        return True

def get_total_bytes(s3, bucket_name, bucket_key):
    file = s3.head_object(Bucket=bucket_name, Key=bucket_key)
    return file["ContentLength"]

def get_object(s3, bucket_name, bucket_key):
    logger = logging.getLogger('views_utils.get_object')

    total_bytes = get_total_bytes(s3, bucket_name, bucket_key)
    if total_bytes > 100000:
        logger.debug(f"Total Bytes: {total_bytes}")
        return get_object_range(s3, total_bytes, bucket_name, bucket_key)
    else:
        return s3.get_object(Bucket=bucket_name, Key=bucket_key)['Body'] \
            .read().decode('utf-8')

def get_object_range(s3, total_bytes, bucket_name, bucket_key):
    logger = logging.getLogger('views_utils.get_object_range')
    offset = 0
    while total_bytes > 0:
        end = offset + 99999 if total_bytes > 100000 else ""
        total_bytes -= 100000
        byte_range = 'bytes={offset}-{end}'.format(offset=offset, end=end)
        logger.debug(f"\tBytes Range: {byte_range}")
        offset = end + 1 if not isinstance(end, str) else None
        yield s3.get_object(Bucket=bucket_name, Key=bucket_key, Range=byte_range)['Body'].read()
