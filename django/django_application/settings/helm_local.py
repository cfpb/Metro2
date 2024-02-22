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

AUTH_ADFS = {
    'AUDIENCE': 'client_id',
    'CLIENT_ID': 'client_id',
    'CLIENT_SECRET': 'client_secret',
    'CLAIM_MAPPING': {'first_name': 'given_name',
                      'last_name': 'family_name',
                      'email': 'email'},
    'GROUPS_CLAIM': 'groups',
    'MIRROR_GROUPS': True,
    'USERNAME_CLAIM': 'email',
    'TENANT_ID': 'tenant_id',
    'RELYING_PARTY_ID': 'client_id',
}
