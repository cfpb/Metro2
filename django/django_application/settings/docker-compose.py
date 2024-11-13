from .base import *

DEBUG = True

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'metro2-data',
        'USER': 'postgres',
        'PASSWORD': 'cfpb',
        'HOST': 'postgres',
        'PORT': '5432'
    }
}
S3_ENABLED=False
S3_BUCKET_NAME = "cfpb-metro2-***REMOVED***"
LOCAL_EVENT_DATA = "parse_m2/local_data/"

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'django']

SETTINGS_DIR = Path(__file__).resolve().parent
AWS_CREDS_LOCATION = [
    SETTINGS_DIR / 'aws-svc-access-key.txt',
    SETTINGS_DIR / 'aws-svc-secret-key.txt',
]