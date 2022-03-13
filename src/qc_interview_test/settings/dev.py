from qc_interview_test.settings.base import *
import os

from dotenv import load_dotenv

load_dotenv()

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DATABASE_HOST'),
        'USER': os.environ.get('DATABASE_USERNAME'),
        'NAME': os.environ.get('DATABASE_NAME'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'PORT': 5432,
    },
}

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
  'http://localhost:8887',
  'http://127.0.0.1:8887',
  'http://localhost:5500',
  'http://127.0.0.1:5500'
)

ALLOWED_HOSTS=['*']

BACKEND_URL = 'http://localhost:8000'

DEBUG = bool(int(os.environ.get('DEBUG', 0)))


########## CELERY CONFIGS ##############
BROKER_URL = os.environ.get('BROKER_URL')
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
BROKER_BACKEND = 'memory'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600, 'fanout_prefix': True, 'fanout_patterns': True}  # 1 hour

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'