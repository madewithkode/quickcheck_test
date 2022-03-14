from django.urls import path
from hackernews.api.views import (
    LatestNews,
    NewsSearchByTitle,
    CreateItem,
    DeleteItem,
    UpdateItem

)


urlpatterns = [

    path('items/', LatestNews.as_view(), name='latest_news'),
    path('update/', UpdateItem.as_view(), name='update_item'),
    path('add/', CreateItem.as_view(), name='add_item'),
    path('search/', NewsSearchByTitle.as_view(), name='news_search'),
    path('delete/<str:item_id>/', DeleteItem.as_view(), name='delete_item'),

]

