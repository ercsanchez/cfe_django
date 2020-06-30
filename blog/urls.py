from django.urls import path
from .views import home_view, redirect_view

app_name = 'blog'

urlpatterns = [
    path('', home_view, name='home-view'),
    path('redirect/', redirect_view, name='redirect')
]