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

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ]
}

LOCAL_EVENT_DATA = "parse_m2/local_data/"
