from datetime import datetime, timedelta
from django.urls import reverse
from django.test import TestCase
from http import HTTPStatus
from webapp.models import Client, Payment
from webapp.forms import PaymentForm


class PaymentCreateTest(TestCase):
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

        self.payment1 = Payment.objects.create(
            client=self.client1,
            amount=500,
            paid_at=datetime.now() - timedelta(days=14)
        )

        self.payment2 = Payment.objects.create(
            client=self.client2,
            amount=1000,
            paid_at=datetime.now() - timedelta(days=10)
        )

    def test_payment_create(self):
        data = {
            'amount': 2000
        }

        url = reverse('webapp:payment_create', kwargs={'pk': self.client3.pk})
        response = self.client.post(url, data=data)
        payment_form = PaymentForm(data=data)
        self.assertTrue(payment_form.is_valid())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Payment.objects.count(), 3)

    def test_payment_update(self):
        data = {
            'amount': 2000
        }

        url = reverse('webapp:payment_update', kwargs={'pk': self.payment2.pk})
        response = self.client.post(url, data=data)
        payment_form = PaymentForm(data=data)
        self.assertTrue(payment_form.is_valid())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.payment2.refresh_from_db()
        self.assertEqual(self.payment2.amount, 2000)

    def test_payment_delete(self):
        url = reverse('webapp:payment_delete', kwargs={'pk': self.payment1.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(Payment.objects.filter(pk=self.payment1.pk).exists())
