import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from .models import Link
from .serializers import LinkSerializer


class ShortenURLTests(APITestCase):
    def setUp(self):
        self.create_url = reverse('shorten_url')
        self.list_url = reverse('list_all_links')
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_shorten_url_creation(self):
        data = {'original_url': 'http://example.com/'}
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Link.objects.count(), 1)
        self.assertEqual(Link.objects.get().original_url, 'http://example.com/')

    def test_redirect_original_url(self):
        link = Link.objects.create(original_url='http://example.com/', short_code='abc123')
        url = reverse('redirect_original', kwargs={'short_code': link.short_code})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), LinkSerializer(link).data)

    def test_delete_link(self):
        link = Link.objects.create(original_url='http://example.com/', short_code='abc123')
        url = reverse('link_edit_delete', kwargs={'pk': link.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Link.objects.count(), 0)

    def test_list_all_links(self):
        Link.objects.create(original_url='http://example.com/', short_code='abc123')
        Link.objects.create(original_url='http://example.org/', short_code='def456')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
