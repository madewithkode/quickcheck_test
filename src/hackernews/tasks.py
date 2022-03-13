from hackernews.hacker_news_adaptor import HackerNewsAdaptor
from qc_interview_test.settings.celery import CELERY

from celery.utils.log import get_task_logger

logging = get_task_logger(__name__)

@CELERY.task(name='ingest_new_data')
def ingest_new_data():
    """
    Ingest new data from HackerNews to db.
    """

    adaptor = HackerNewsAdaptor()
    adaptor.ingest_data()