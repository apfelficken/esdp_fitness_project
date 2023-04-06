from django.views.generic import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from webapp.models import Client, Payment
from webapp.forms import PaymentForm
from django.http import HttpResponseRedirect


class PaymentCreateView(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name: str = 'payments/payment_create.html'

    def form_valid(self, form):
        client = get_object_or_404(Client, pk=self.kwargs.get('pk'))
        form.instance.client = client
        response = super().form_valid(form)
        if client.payment_end_date is None:
            client.payment_end_date = timezone.now() + timedelta(days=30)
        elif client.payment_end_date > timezone.now():
            client.payment_end_date = client.payment_end_date + timedelta(days=30)
        else:
            client.payment_end_date = timezone.now() + timedelta(days=30)
        client.save()
        return response

    def get_success_url(self) -> str:
        return reverse('webapp:client_detail', kwargs={'pk': self.object.client.pk})


class PaymentUpdateView(UpdateView):
    model = Payment
    template_name: str = 'payments/payment_update.html'
    form_class = PaymentForm

    def get_success_url(self) -> str:
        return reverse('webapp:client_detail', kwargs={'pk': self.object.client.pk})


class PaymentDeleteView(DeleteView):
    model = Payment
    template_name = 'payments/payment_delete.html'

    def form_valid(self, form):
        success_url = self.get_success_url()
        payment = self.get_object()
        client = payment.client
        newest_payment = client.payments.order_by('-paid_at').first()
        if newest_payment == payment:
            client.payment_end_date = client.payment_end_date - timedelta(days=30)
            client.save()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_success_url(self) -> str:
        return reverse('webapp:client_detail', kwargs={'pk': self.object.client.pk})
