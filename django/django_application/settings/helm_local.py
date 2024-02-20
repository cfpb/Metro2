# Use these settings when running the helm chart on your local computer for testing.

from .base import *
from .base import MIDDLEWARE as BASE_MIDDLEWARE

import os

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

# Client secret is not public information. Should store it as an environment variable.

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
tenant_id = os.getenv('TENANT_ID')


AUTH_ADFS = {
    'AUDIENCE': client_id,
    'CLIENT_ID': client_id,
    'CLIENT_SECRET': client_secret,
    'CLAIM_MAPPING': {'first_name': 'given_name',
                      'last_name': 'family_name',
                      'email': 'email'},
    'GROUPS_CLAIM': 'groups',
    'MIRROR_GROUPS': True,
    # "GROUP_TO_FLAG_MAPPING": {"is_staff": ["a5bd2882-06e9-4b4a-9c56-c263eceaf458"],
    #                           "is_superuser": "e35164c7-4aa7-40a3-8ff7-064425ac68e5"},
    'USERNAME_CLAIM': 'email',
    'TENANT_ID': tenant_id,
    'RELYING_PARTY_ID': client_id,
}

AUTHENTICATION_BACKENDS = [
    'django_auth_adfs.backend.AdfsAuthCodeBackend',
    'django_auth_adfs.backend.AdfsAccessTokenBackend',
]

MIDDLEWARE = BASE_MIDDLEWARE + [
    'django_auth_adfs.middleware.LoginRequiredMiddleware',
]

# Configure django to redirect users to the right URL for login
LOGIN_URL = "django_auth_adfs:login"
LOGIN_REDIRECT_URL = "/"
