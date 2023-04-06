from datetime import datetime, timedelta
from django.urls import reverse
from django.test import TestCase
from http import HTTPStatus
from webapp.models import Client, Training, Group


class TrainingTest(TestCase):
    def setUp(self) -> None:
        self.client1 = Client.objects.create(
            telegram_name='client1',
            phone='test_data',
            first_name='test_data',
            last_name='test_data',
            email='test_data',
            payment_end_date=datetime.now() + timedelta(days=10),
            region='test_data',
            comment='test_data'
        )

        self.client2 = Client.objects.create(
            telegram_name='client2',
            phone='test_data',
            first_name='test_data',
            last_name='test_data',
            email='test_data',
            payment_end_date=datetime.now() + timedelta(days=10),
            region='test_data',
            comment='test_data'
        )

        self.client3 = Client.objects.create(
            telegram_name='client3',
            phone='test_data',
            first_name='test_data',
            last_name='test_data',
            email='test_data',
            payment_end_date=datetime.now() + timedelta(days=15),
            region='test_data',
            comment='test_data'
        )

        self.group1 = Group.objects.create(
            name='Gym',
            start_at='18:00'
        )

        self.group2 = Group.objects.create(
            name='UFC',
            start_at='19:00'
        )

        self.training1 = Training.objects.create(
            client=self.client1,
            date='2023-03-30',
            group=self.group1
        )

        self.training2 = Training.objects.create(
            client=self.client2,
            date='2023-03-31',
            group=self.group2
        )

    def test_training_create(self):
        url = reverse('webapp:training_create', kwargs={'pk': self.client3.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Training.objects.count(), 3)

    def test_training_list(self):
        url = reverse('webapp:training_list', kwargs={'pk': self.client1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_training_delete(self):
        url = reverse('webapp:training_delete', kwargs={'pk': self.training1.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(Training.objects.filter(pk=self.training1.pk).exists())
