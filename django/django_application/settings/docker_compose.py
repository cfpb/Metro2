import sys
from .base import *

DEBUG = True
TESTING = "test" in sys.argv

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"].append(
    'rest_framework.renderers.BrowsableAPIRenderer'
)

# If DEBUG is enabled and we're not running tests, add Django Debug Toolbar
if DEBUG and not TESTING:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG,
        "UPDATE_ON_FETCH": True,
    }
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.history.HistoryPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
    ]

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
