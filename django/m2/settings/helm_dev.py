from .base import *


DEBUG = True

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "metro2-results",
        "USER": "postgres",
        "PASSWORD": "cfpb",
        "HOST": "results-db-postgresql",
        "PORT": "5432",
    }
}