from django.contrib import admin

from shortener.models import Link
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']
admin.site.register(Link)