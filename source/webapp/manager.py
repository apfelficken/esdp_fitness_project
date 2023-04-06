from datetime import datetime
from django.db import models


class ActiveClientManager(models.Manager):
    def active_clients(self):
        return super().get_queryset().filter(payment_end_date__gt=datetime.now())
