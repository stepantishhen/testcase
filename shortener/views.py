import random
import string

from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Link
from .serializers import LinkSerializer


class ShortenURLView(generics.CreateAPIView):
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={201: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING),
                'link': openapi.Schema(type=openapi.TYPE_OBJECT, properties={})  # Define your model properties here
            }
        )}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        original_url = serializer.validated_data.get('original_url')

        link = Link(original_url=original_url)
        link.short_code = generate_short_code()
        link.save()

        serialized_link = LinkSerializer(link).data  # Serialize the link instance

        response_data = {
            "message": "OK",
            "link": serialized_link  # Include serialized link data in the response
        }

        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class RedirectOriginalView(generics.RetrieveAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'short_code'  # Define the lookup field

    def retrieve(self, request, *args, **kwargs):
        link = self.get_object()
        serialized_link = self.get_serializer(link).data
        return Response(serialized_link, status=status.HTTP_200_OK)


class LinkEditDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class ListAllLinksView(generics.ListAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['users']

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.query_params.get('sort_by')
        if sort_by == 'created_at':
            queryset = queryset.order_by('created_at')
        return queryset


def generate_short_code():
    characters = string.ascii_letters + string.digits
    short_code = ''.join(random.choice(characters) for _ in range(6))
    return short_code
