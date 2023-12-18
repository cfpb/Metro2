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

S3_BUCKET_NAME = "cfpb-metro2-***REMOVED***"
