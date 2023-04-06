from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from constance import config
import json


class AdminViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('api_v1:cache')

    def test_no_cached_data(self) -> None:
        config.ADMIN = None

        response = self.client.get(self.url)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(data, {'error': 'No cached data found'})

    def test_get_valid_cached_data(self) -> None:
        cached_data: int = 123
        config.ADMIN = cached_data

        response = self.client.get(self.url)
        data = json.loads(response.content)

        self.assertIsInstance(data, int)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, cached_data)

    def test_get_invalid_cached_data(self) -> None:
        cached_data: str = 'kek'
        config.ADMIN = cached_data

        response = self.client.get(self.url)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data, {'error': 'Invalid data'})
