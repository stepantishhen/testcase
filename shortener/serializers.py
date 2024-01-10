from django.core.validators import URLValidator
from rest_framework import serializers
from shortener.models import Link


class LinkSerializer(serializers.ModelSerializer):
    original_url = serializers.CharField(validators=[URLValidator()])
    short_code = serializers.CharField(required=False)

    class Meta:
        model = Link
        fields = ('pk', 'original_url', 'short_code', 'created_at')