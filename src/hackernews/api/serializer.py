from datetime import datetime
from email.policy import default
from rest_framework import serializers
from hackernews.models import Hackernews, generate_unique_id
import os
from django.conf import settings


class StorySerializer(serializers.Serializer):
    """
        Serializer for creating/Indexing new stories.
    """

    id = serializers.CharField(default=None)
    content = serializers.CharField(default=None)
    title = serializers.CharField(required=True)
    type = serializers.CharField(required=True)
    by = serializers.CharField(required=True)
    kids = serializers.ListField(
        child=serializers.CharField(default=None), default=[]
    )
    time = serializers.IntegerField(default=None)  # Original HackerNews time (UNIX time),defaults to None if not provided i.e not a HN story
    url = serializers.CharField(default=None)


    def create(self, validated_data):
        # Create local unique id for story
        unique_id  =  generate_unique_id()
        try:
            return Hackernews.objects.create(
                id = unique_id,
                hackernews_id = validated_data['id'], # This would default to None if not provided i.e stories that are not from HN
                content = validated_data['content'],
                title = validated_data['title'],
                type = validated_data['type'],
                by = validated_data['by'],
                kids = validated_data['kids'], # This would default to an empty list if not provided i.e if the story is not from HN or if it doesn't have kids
                indexed_time = datetime.now(), # This is the time an entry was made to the db, whether it's a HN story or not.
                published_time = validated_data['time'],
                url = validated_data['url'] if validated_data['url'] else None
            )
        except Exception as e:
            raise Exception("An error ocured while indexing data {}".format(e))

    def update(self, instance, validated_data):
        instance.content = validated_data['content'] if validated_data['content'] else instance.content
        instance.title = validated_data['title'] if validated_data['title'] else instance.title
        instance.type = validated_data['type'] if validated_data['type'] else instance.type
        instance.by = validated_data['by'] if validated_data['by'] else instance.by
        instance.kids = validated_data['kids'] if validated_data['kids'] else instance.kids
        instance.save()

        return instance

class StoryTypeFilterSerializer(serializers.ModelSerializer):
    """
        Serializer for returning stories based on their type.
    """

    class Meta:
        model = Hackernews
        fields = ['id', 'hackernews_id', 'content', 'title', 'type', 'by', 'kids', 'indexed_time', 'published_time', 'url']
