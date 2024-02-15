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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'prepend_date': {
            'format': '{asctime} {levelname}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'prepend_date',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
