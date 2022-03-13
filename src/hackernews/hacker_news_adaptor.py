import string
import random
from django.conf import settings
import requests
import json
from hackernews.api.serializer import StorySerializer
from hackernews.models import Hackernews

from celery.utils.log import get_task_logger

logging = get_task_logger(__name__)

class HackerNewsAdaptor:

    HACKER_NEWS_BASE_API = 'https://hacker-news.firebaseio.com/v0/'

    def ingest_data(self, is_first_time=False):
        '''
            This method ingests news items from Hacker News.
        '''

        try:
            response = requests.get('{}/topstories.json?print=pretty'.format(self.HACKER_NEWS_BASE_API))
            if response:
                latest_stories_list = response.json()
        except TimeoutError:
            raise Exception("The request timed out, try again later.")

        if latest_stories_list:
            # try to get hackernews ids for all indexed data if they exist
            q = Hackernews.objects.all().distinct('hackernews_id')
            existing_data_list = [x.hackernews_id for x in q if not x.hackernews_id == None]
        
            story_count = 0
            
            n = 100 if is_first_time else 10
            # Ingest latest 100 items from HN for the first time else ingest lates 10 periodically.
            for i in latest_stories_list[:n]:
                if i in existing_data_list:
                    logging.info('Already Indexed data - {}, Skipping....'.format(i))
                    print('Already Indexed data - {}, Skipping....'.format(i))
                    continue # Skip already indexed stories
                else:
                    try:
                        inner_response = requests.get('{}/item/{}.json?print=pretty'.format(self.HACKER_NEWS_BASE_API, i))
                        if inner_response.status_code == 200:
                            logging.info('success!')
                        elif inner_response.status_code == 404:
                            logging.info('Resource Not Found.')
                            print('Resource Not Found.')
                            return
                        else:
                            logging.info('An error has occurred.')
                            print('An error has occurred.')
                            return
                    except TimeoutError:
                        raise Exception("The request timed out, try again later.")
                    
                    try:
                        serializer = StorySerializer(data=inner_response.json())
                        serializer.is_valid(raise_exception=True)
                        story = serializer.save()
                        if not story:
                            raise Exception("An error ocured while indexing data")
                        logging.info('Successfully Indexed Hackernews {}'.format(story))
                        print('Successfully Indexed Hackernews {}'.format(story))
                        story_count += 1
                    except Exception as e:
                        raise Exception("An error ocured {}".format(e))
            if story_count == 0:
                logging.info('No new story to index at this time.')
                print('No new story to index at this time.')
                return
            logging.info('Inexed a total of {} new stories'.format(story_count))
            print('Inexed a total of {} new stories'.format(story_count))
            return


