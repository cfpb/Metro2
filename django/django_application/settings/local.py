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

SETTINGS_DIR = Path(__file__).resolve().parent
AWS_CREDS_LOCATION = [
    SETTINGS_DIR / 'aws-svc-access-key.txt',
    SETTINGS_DIR / 'aws-svc-secret-key.txt',
]

LOGGING['root']= {
        'handlers': ['console'],
        'level': 'DEBUG',
    }