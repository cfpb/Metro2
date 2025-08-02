from .base import *

DEBUG = True

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LOCAL_EVENT_DATA = Path().resolve() / "sample_data"

LOGGING['root']= {
        'handlers': ['console'],
        'level': 'DEBUG',
    }

# Un-comment the following settings when testing S3 locally.
# You will need to add AWS service account keys to your settings directory.
# S3_BUCKET_NAME = f"cfpb-metro2-***REMOVED***"
# S3_ENABLED=True
# SETTINGS_DIR = Path(__file__).resolve().parent
# AWS_CREDS_LOCATION = [
#     SETTINGS_DIR / 'aws-svc-access-key.txt',
#     SETTINGS_DIR / 'aws-svc-secret-key.txt',
# ]
