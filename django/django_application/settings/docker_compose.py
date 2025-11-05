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

LOCAL_EVENT_DATA = Path().resolve() / "sample_data"

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'django']

# Un-comment the following settings when testing S3 locally.
# You will also need to provide credentials. See s3_utils.py for more information.
# S3_ENABLED=True
# S3_BUCKET_NAME = "bucket-name"
