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

LOCAL_EVENT_DATA = "parse_m2/local_data/"
S3_BUCKET_NAME = "cfpb-metro2-***REMOVED***"
S3_ENABLED=False

LOGGING['root']= {
        'handlers': ['console'],
        'level': 'DEBUG',
    }

# Use front end modules served by vite instead of built assets
DJANGO_VITE_DEV_MODE = True
