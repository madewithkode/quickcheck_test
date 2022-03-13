from django.core.management.base import BaseCommand
from hackernews.hacker_news_adaptor import HackerNewsAdaptor

class Command(BaseCommand):
    help = 'Ingests latest 100 articles from HackerNews. This is meant to be called after project setup.'

    def handle(self, *args, **kwargs):
        print('Preparing to Index lastes 100 items from HackerNews....')
        adaptor = HackerNewsAdaptor()
        adaptor.ingest_data(is_first_time=True)
