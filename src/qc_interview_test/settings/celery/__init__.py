import os
from django.conf import settings
from celery import Celery
from celery.schedules import crontab


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qc_interview_test.settings.dev')


CELERY = Celery('qc_interview_test')

CELERYBEAT_SCHEDULE = {
    # Ingest new data Every 5 minutes
    'ingest_new_data': {
        'task': 'ingest_new_data',
        'schedule': crontab(minute="*/5"),
    },
}


CELERY.config_from_object('django.conf:settings')
CELERY.conf.update(CELERYBEAT_SCHEDULE=CELERYBEAT_SCHEDULE)
CELERY.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
