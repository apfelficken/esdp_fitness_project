import django_filters
from django.db.models import Q
from .models import Client
from datetime import datetime


CHOICES = (
    (0, 'All'),
    (1, 'Paid'),
    (2, 'Unpaid')
)


class ClientFilter(django_filters.FilterSet):
    is_paid = django_filters.ChoiceFilter(
        choices=CHOICES,
        label='Оплата',
        method='filter_is_paid',
        empty_label=None
        )

    class Meta:
        model = Client
        fields = ['is_paid']

    def filter_is_paid(self, queryset, name, val):
        if val == '1':
            return queryset.filter(payment_end_date__gt=datetime.now())
        if val == '2':
            return queryset.filter(Q(payment_end_date__lte=datetime.now()) | Q(payment_end_date__isnull=True))
        return queryset
