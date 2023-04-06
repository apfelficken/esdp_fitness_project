from datetime import datetime, timedelta
from django.urls import reverse
from django.test import TestCase
from http import HTTPStatus
from webapp.models import Coach
from webapp.forms import CoachForm


class CoachTest(TestCase):
    def setUp(self) -> None:
        self.coach1 = Coach.objects.create(
            telegram_name='coach1',
            phone='test_data',
            first_name='test_data',
            last_name='test_data',
            email='test@data.com',
            started_to_work=(datetime.now() - timedelta(days=6)).strftime('%Y-%m-%d'),
            description='test_data',
            )

        self.coach2 = Coach.objects.create(
            telegram_name='coach2',
            phone='test_data',
            first_name='test_data',
            last_name='test_data',
            email='test@data.com',
            started_to_work=(datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
            description='test_data',
        )

    def test_coach_create(self):
        data = {
            "telegram_name": 'coach3',
            "phone": 'test_data',
            "first_name": 'test_data',
            "last_name": 'test_data',
            "email": 'test@data.com',
            "started_to_work": (datetime.now()).strftime('%Y-%m-%d'),
            "description": 'test_data',
        }

        url = reverse('webapp:coach_create')
        response = self.client.post(url, data=data)
        coach_form = CoachForm(data=data)
        self.assertTrue(coach_form.is_valid())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Coach.objects.count(), 3)

    def test_coach_no_telegram_name_create(self):
        data = {
            "telegram_name": 'coach3',
            "phone": 'test_data',
            "first_name": 'test_data',
            "last_name": 'test_data',
            "email": 'test@data.com',
            "started_to_work": '',
            "description": 'test_data',
        }

        url = reverse('webapp:coach_create')
        response = self.client.post(url, data=data)
        coach_form = CoachForm(data=data)
        self.assertFalse(coach_form.is_valid())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_coach_no_start_date_create(self):
        data = {
            "telegram_name": '',
            "phone": 'test_data',
            "first_name": 'test_data',
            "last_name": 'test_data',
            "email": 'test@data.com',
            "started_to_work": (datetime.now()).strftime('%Y-%m-%d'),
            "description": 'test_data',
        }

        url = reverse('webapp:coach_create')
        response = self.client.post(url, data=data)
        coach_form = CoachForm(data=data)
        self.assertFalse(coach_form.is_valid())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_coach_update(self):
        data = {
            "telegram_name": 'coach2',
            "phone": 'updated_data',
            "first_name": 'updated_data',
            "last_name": 'updated_data',
            "email": 'updated@data.com',
            "started_to_work": (datetime.now() - timedelta(days=25)).strftime('%Y-%m-%d'),
            "description": 'updated_data',
        }

        url = reverse('webapp:coach_update', kwargs={'pk': self.coach1.pk})
        response = self.client.post(url, data=data)
        coach_form = CoachForm(data=data)
        self.assertTrue(coach_form.is_valid())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.coach1.refresh_from_db()
        self.assertEqual(self.coach1.last_name, 'updated_data')

    def test_coach_list(self):
        url = reverse('webapp:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_coach_detail(self):
        url = reverse('webapp:coach_detail', kwargs={'pk': self.coach1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_coach_delete(self):
        url = reverse('webapp:coach_delete', kwargs={'pk': self.coach1.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(Coach.objects.filter(pk=self.coach1.pk).exists())
