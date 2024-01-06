from rest_framework import serializers
from shortener.models import Link


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('original_url', 'short_code', 'created_at')