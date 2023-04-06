from datetime import datetime, timedelta
from django.urls import reverse
from django.test import TestCase
from http import HTTPStatus
from webapp.models import Group, Client
from webapp.forms import GroupForm


class GroupTest(TestCase):
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

        self.group1 = Group.objects.create(
            name='Gym',
            start_at='18:00'
        )

        self.group2 = Group.objects.create(
            name='UFC',
            start_at='19:00'
        )

    def test_group_create(self):
        data = {
            'name': 'Dancing',
            'start_at': '19:00'
        }

        url = reverse('webapp:group_create')
        response = self.client.post(url, data=data)
        group_form = GroupForm(data=data)
        self.assertTrue(group_form.is_valid())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Group.objects.count(), 3)

    def test_group_update(self):
        data = {
            'name': 'Warm Up',
            'start_at': '17:00'
        }

        url = reverse('webapp:group_update', kwargs={'pk': self.group1.pk})
        response = self.client.post(url, data=data)
        group_form = GroupForm(data=data)
        self.assertTrue(group_form.is_valid())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.group1.refresh_from_db()
        self.assertEqual(self.group1.name, 'Warm Up')

    def test_group_client_update(self):
        data = {
            'active_client_id': self.client1.pk
        }
        url = reverse('webapp:group_client_update', kwargs={'pk': self.group1.pk})
        response = self.client.post(url, data=data)
        self.client1.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(self.client1.group.pk, self.group1.pk)

    def test_group_list(self):
        url = reverse('webapp:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_group_detail(self):
        url = reverse('webapp:group_detail', kwargs={'pk': self.group1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_group_delete(self):
        url = reverse('webapp:group_delete', kwargs={'pk': self.group1.pk})
        response = self.client.post(url)
        self.group1.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(self.group1.is_active)

    def test_group_client_delete(self):
        self.client1.group = self.group1
        self.client1.save()
        url = reverse('webapp:group_client_delete', kwargs={'pk': self.client1.pk})
        response = self.client.get(url)
        self.client1.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(self.client1.group)
