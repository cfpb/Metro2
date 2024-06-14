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
LOCAL_EVENT_DATA = "parse_m2/local_data/"

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'django']
