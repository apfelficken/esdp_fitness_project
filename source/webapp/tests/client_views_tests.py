from datetime import datetime, timedelta
from django.urls import reverse
from django.test import TestCase
from http import HTTPStatus
from webapp.models import Client, Group
from webapp.forms import ClientForm, AddGroupClient


class ClientTest(TestCase):
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

        self.group1 = Group.objects.create(
            name='Gym',
            start_at='18:00'
        )

    def test_client_create(self):
        data = {
            'telegram_name': 'client3',
            'phone': 'test_data',
            'first_name': 'test_data',
            'last_name': 'test_data',
            'email': 'test@data.com',
            'payment_end_date': (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d'),
            'region': 'test_data',
            'comment': 'test_data'
        }

        url = reverse('webapp:client_create')
        response = self.client.post(url, data=data)
        client_form = ClientForm(data=data)
        self.assertTrue(client_form.is_valid())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Client.objects.count(), 3)

    def test_client_form_invalid_create(self):
        data = {
            'phone': 'test_data',
            'first_name': 'test_data',
            'last_name': 'test_data',
            'email': 'test@data.com',
            'payment_end_date': (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d'),
            'region': 'test_data',
            'comment': 'test_data'
        }

        url = reverse('webapp:client_create')
        response = self.client.post(url, data=data)
        client_form = ClientForm(data=data)
        self.assertFalse(client_form.is_valid())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_client_update(self):
        data = {
            'telegram_name': 'client3',
            'phone': 'updated_data',
            'first_name': 'updated_data',
            'last_name': 'updated_data',
            'email': 'updated@data.com',
            'payment_end_date': (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d'),
            'region': 'updated_data',
            'comment': 'updated_data'
        }

        url = reverse('webapp:client_update', kwargs={'pk': self.client1.pk})
        response = self.client.post(url, data=data)
        client_form = ClientForm(data=data)
        self.assertTrue(client_form.is_valid())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.client1.refresh_from_db()
        self.assertEqual(self.client1.last_name, 'updated_data')

    def test_client_group_update(self):
        data = {
            'group_id': self.group1.pk
        }
        url = reverse('webapp:client_group_update', kwargs={'pk': self.client1.pk})
        response = self.client.post(url, data=data)
        self.client1.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(self.client1.group.pk, self.group1.pk)

    def test_client_list(self):
        url = reverse('webapp:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_client_detail(self):
        url = reverse('webapp:client_detail', kwargs={'pk': self.client1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_client_delete(self):
        url = reverse('webapp:client_delete', kwargs={'pk': self.client1.pk})
        response = self.client.post(url)
        self.client1.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(self.client1.is_active)
