from django.urls import path

from .views import *

urlpatterns = [
    path('api/shorten/', shorten_url, name="shorten_url"),
    path('api/<str:short_code>/', redirect_original, name='redirect_original'),
    path('', index, name='index')
]
