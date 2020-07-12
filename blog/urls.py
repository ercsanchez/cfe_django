from django.urls import path
from .views import (
    home_view, 
    redirect_view, 
    post_list_view, 
    post_detail_view, 
    post_create_view,
)

app_name = 'blog'

urlpatterns = [
    path('', home_view, name='home-view'),
    path('redirect/', redirect_view, name='redirect'),
    path('posts/', post_list_view, name='post-list-view'),
    path('<int:pk>/', post_detail_view, name='post-detail-view'),
    path('create/', post_create_view, name='post-create-view'),
]