import os

DEBUG = True
TEMPLATE_DEBUG = True

ADMINS = (
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'griddly_dev',                      # Or path to database file if using sqlite3.
        'USER': 'griddly',                      # Not used with sqlite3.
        'PASSWORD': 'dev',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

MEDIA_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, 'site_media', 'media'))
MEDIA_URL = '/site_media/media/'

STATIC_ROOT = '/home/static'

STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 'wholn(f3b+y7t)r=ea407zq8c80lxf-cr++lrb)aub%ml33wi$'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

)

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    'raven.contrib.django.middleware.SentryResponseErrorIdMiddleware',
    'raven.contrib.django.middleware.Sentry404CatchMiddleware',
)

AUTHENTICATION_BACKENDS = ('facebook.backend.FacebookBackend', 'django.contrib.auth.backends.ModelBackend', 'account.backends.auth.GoogleBackend')
#FB LOGIN
AUTH_PROFILE_MODULE = 'facebook.FacebookProfile'
FACEBOOK_APP_ID = '165186856899090'
FACEBOOK_APP_SECRET = 'cce7d92718bc6358211eeffba1ac2529'
FACEBOOK_SCOPE = 'email,publish_stream'
#GOOGLE LOGIN
OPENID_SSO_SERVER_URL = 'https://www.google.com/accounts/o8/id'

ROOT_URLCONF = 'urls'
TEMPLATE_DIRS = ('/home/wok/projects/griddly/templates',)
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/'
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_openid_auth',

    'sentry',
    'raven.contrib.django',

    'feedback',
    'alliance',
    'account',
    'profile',
    'common',
    'game',
    'external-api',
    'nodejs_server',
    'location',
    'checkin',
    'territory',
    'battle',
    'ranks',
    'notification',
    'map',
    'mobile',
    'foursquare',
    'facebook',
)

SENTRY_CLIENT = 'raven.contrib.django.DjangoClient'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'DEBUG',
            'class': 'raven.contrib.django.logging.SentryHandler',
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

import logging
from raven.contrib.django.logging import SentryHandler
logger = logging.getLogger()
if SentryHandler not in map(type, logger.handlers):
    logger.addHandler(SentryHandler())

    logger = logging.getLogger('sentry.errors')
    logger.propagate = False
    logger.addHandler(logging.StreamHandler())