from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField
import string
import random

# Create your models here.

def generate_unique_id(length=8):
    """
        Generate random unique alphanumeric Ids.
    """
    
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

class Hackernews(models.Model):
    """
        Model representation for a Hackernews story.
    """

    id = models.CharField(primary_key=True, max_length=100, default=generate_unique_id, unique=True, editable=False)
    hackernews_id = models.IntegerField(null=True)
    title = models.TextField()
    content = models.TextField(null=True)
    type = models.CharField(max_length=200)
    by = models.CharField(max_length=200)
    kids = ArrayField(models.CharField(max_length=100), null=True)
    indexed_time = models.DateTimeField(null=True)
    published_time = models.IntegerField(null=True) # Original time published on HackerNews (UNIX time)
    url = models.TextField(null=True)

    def __str__(self):
        """Respresentation of Hackernews Story.
        """

        return 'Story - {}'.format(self.title)
