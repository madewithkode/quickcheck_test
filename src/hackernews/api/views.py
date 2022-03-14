from django.shortcuts import render
from hackernews.api.serializer import StorySerializer, StoryTypeFilterSerializer
from hackernews.models import Hackernews
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import filters
from hackernews.utils import CustomPagination
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

class LatestNews(ListAPIView):
    """
    This view returns a list of all the latest
    indexed/published news with an optional type
    filter.
    """

    serializer_class = StoryTypeFilterSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        type = self.request.query_params.get('type')
        if type:
            return Hackernews.objects.filter(type=type.lower()).order_by('-indexed_time')
        return Hackernews.objects.all().order_by('-indexed_time')

class NewsSearchByTitle(ListAPIView):
    """
    This view is used to search News by text contained
    either in title or content.
    """

    serializer_class = StoryTypeFilterSerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = CustomPagination
    queryset = Hackernews.objects.all()
    search_fields = ['title', 'content']
    

class CreateItem(APIView):
    """
        This endpoint creates new item/news locally.
    """

    serializer_class = StorySerializer

    @swagger_auto_schema(request_body=StorySerializer)
    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.save()

        if validated_data:
            return Response(
                {
                    'status': True,
                    'message': 'New {} added successfully.'.format(validated_data),
                    'id': validated_data.id
                },
                status=status.HTTP_200_OK,
            )
        return Response(
                {
                    'status': False,
                    'message': 'An error occured, try again later.'
                },
                status=status.HTTP_200_OK,
            )

class UpdateItem(APIView):
    """
    Update items created via the API not fetched from HackerNews.
    """

    serializer_class = StorySerializer

    @swagger_auto_schema(request_body=StorySerializer)
    def put(self, request):

        if not 'id' in request.data or request.data['id'] == None:
            return Response(
                {
                    'status': False,
                    'message': 'id field is required to update an item.'
                },
                status=status.HTTP_200_OK,
            )

        try:
           # fetch the record instance
            record = Hackernews.objects.get(
                id=request.data['id']
            )

            # confirm record is not fetched from HN and deny edit access if true.
            if record.hackernews_id:
                return Response(
                {'status': False, 'message': 'Cannot update items indexed from HackerNews.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        # if multiple records were found
        except Hackernews.DoesNotExist:
            return Response({'status': False, 'message': 'Item Not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(record, data=request.data)
        serializer.is_valid(raise_exception=True)

        item = serializer.save()

        if not item:
            return Response(
                {'status': False, 'message': 'An error occurred, try again'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                'status': True,
                'message': 'item {} updated successfully'.format(item.id)
            },
            status=status.HTTP_201_CREATED,
        )

class CreateItem(APIView):
    """
        Create item from API
    """

    serializer_class = StorySerializer
    
    @swagger_auto_schema(request_body=StorySerializer)
    def post(self, request):
        
        if not 'content' in request.data or request.data['content'] == None:
            return Response(
                {
                    'status': False,
                    'message': 'content field is required when creating item from API.'
                },
                status=status.HTTP_200_OK,
            )
        
        try:
            Hackernews.objects.get(title=request.data['title'], by=request.data['by'])
            return Response(
                {
                    'status': False,
                    'message': 'Unable to add item, an item with same title and author already exists.'
                },
                status=status.HTTP_200_OK,
            )
        except Hackernews.DoesNotExist:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            validated_data = serializer.save()

            if not validated_data:
                return Response(
                    {
                        'status': False,
                        'message': 'An error occured'
                    },
                    status=status.HTTP_200_OK,
                )
                
            return Response(
                {
                    'status': True,
                    'message': 'Item {} created successfully.'.format(validated_data.id),
                },
                status=status.HTTP_200_OK,
            )
 
class DeleteItem(APIView):
    """
        Delete locally created item.
    """
    @swagger_auto_schema()
    def delete(self, request, item_id):

        try:
            item = Hackernews.objects.get(id=item_id)
            if item.hackernews_id:
                return Response(
                    {'status': False, 'message': 'Unable to delete externally fetched item.'},
                    status=status.HTTP_200_OK,
                )
            else:
                deleted_item_id = item.id
                item.delete()
                return Response(
                    {'status': True, 'message': 'Item {} deleted successfully.'.format(deleted_item_id)},
                    status=status.HTTP_200_OK,
                )
        except Hackernews.DoesNotExist:
            return Response(
                {'status': False, 'message': 'Item does not exist'},
                status=status.HTTP_200_OK,
            )
            