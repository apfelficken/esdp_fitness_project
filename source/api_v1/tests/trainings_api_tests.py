from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import datetime, timedelta
from webapp.models import Client, Group, Training
from api_v1.serializers import TrainingSerializer


class TrainingCreateAPIViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.group = Group.objects.create(name='Test Group', start_at=datetime.now().time())
        self.client1 = Client.objects.create(telegram_name='client1', group=self.group, payment_end_date=datetime.now() + timedelta(days=1))
        self.url = reverse('api_v1:training_create')

    def test_create_training(self) -> None:
        data: dict = {'telegram_name': 'client1'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Training.objects.count(), 1)
        self.assertEqual(Training.objects.first().client, self.client1)

    def test_create_training_invalid_client(self) -> None:
        data: dict = {'telegram_name': 'kek'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Training.objects.count(), 0)

    def test_create_training_missing_telegram_name(self) -> None:
        data: dict = {}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Training.objects.count(), 0)

    def test_create_training_serializer(self) -> None:
        data: dict = {'telegram_name': 'client1'}
        serializer = TrainingSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        training = serializer.save()
        self.assertEqual(Training.objects.count(), 1)
        self.assertEqual(training.client, self.client1)
