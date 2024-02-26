# Use these settings when running the helm chart on your local computer for testing.

from .base import *


DEBUG = True

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "metro2-data",
        "USER": "postgres",
        "PASSWORD": "cfpb",
        "HOST": "metro2-db-postgresql",
        "PORT": "5432",
    }
}

LOCAL_EVENT_DATA = "parse_m2/local_data/"
S3_BUCKET_NAME = "cfpb-metro2-***REMOVED***"

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ]
}
