from .base import *
from .base import MIDDLEWARE as BASE_MIDDLEWARE

import os

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

LOCAL_EVENT_DATA = "parse_m2/local_data/"

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
    "GROUP_TO_FLAG_MAPPING": {"is_staff": ["389cd9aa-2850-41bd-b1a3-d2a6db5020bc",
                                           "9d37ddbb-9ffc-434c-826f-8aac7a740957"],
                              "is_superuser": "9d37ddbb-9ffc-434c-826f-8aac7a740957"},
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
