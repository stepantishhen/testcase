from django.urls import path
from .views import *

urlpatterns = [
    path('shorten/', ShortenURLView.as_view(), name="shorten_url"),
    path('redirect/<str:short_code>/', RedirectOriginalView.as_view(), name='redirect_original'),
    path('link/<int:pk>/', LinkEditDeleteView.as_view(), name='link_edit_delete'),  # Use the primary key for editing/deleting
    path('links/', ListAllLinksView.as_view(), name='list_all_links')
]
