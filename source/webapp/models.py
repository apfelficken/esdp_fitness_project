from django.db import models
from .manager import ActiveClientManager
from .abstract_models import CreatedAndUpdatedTime


class Coach(models.Model):
    telegram_name = models.CharField(max_length=50, blank=False, null=False, verbose_name='Telegram')
    photo = models.ImageField(null=True, blank=True, upload_to='photos', verbose_name='Фото')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер')
    first_name = models.CharField(max_length=20, blank=False, null=False, verbose_name='Имя')
    last_name = models.CharField(max_length=20, blank=True, null=True, verbose_name='Фамилия')
    email = models.EmailField(null=True, blank=True, verbose_name='Email')
    started_to_work = models.DateField(blank=False, null=False, verbose_name='Начало работы')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return f'{self.first_name}'


class Group(models.Model):
    name = models.CharField(max_length=77, blank=False, null=False, verbose_name='Название группы')
    start_at = models.TimeField(blank=False, null=False, verbose_name='Время занятий')
    coach = models.ForeignKey(Coach, blank=True, null=True, on_delete=models.SET_NULL, related_name='groups',
                              verbose_name='Тренер')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} | {self.start_at} | {self.coach}'


class GroupTraining(CreatedAndUpdatedTime):
    coach = models.ForeignKey(Coach, blank=True, null=True, on_delete=models.CASCADE, related_name='coach_trainings',
                              verbose_name='Тренер')
    group = models.ForeignKey(Group, blank=True, null=True, on_delete=models.CASCADE, related_name='group_trainings',
                              verbose_name='Группа')


class Client(CreatedAndUpdatedTime):
    telegram_name = models.CharField(max_length=50, blank=False, null=False, verbose_name='Telegram')
    photo = models.ImageField(null=True, blank=True, upload_to='photos', verbose_name='Фото')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер')
    first_name = models.CharField(max_length=20, blank=True, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=20, blank=True, null=True, verbose_name='Фамилия')
    email = models.EmailField(null=True, blank=True, verbose_name='Email')
    payment_end_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания оплаты')
    region = models.CharField(max_length=50, blank=True, null=True, verbose_name='Регион')
    is_active = models.BooleanField(default=True)
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')
    group = models.ForeignKey(Group, blank=True, null=True, on_delete=models.SET_NULL, related_name='clients',
                              verbose_name='Группа')
    objects = ActiveClientManager()

    def __str__(self):
        return f'{self.telegram_name}'


class Payment(CreatedAndUpdatedTime):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='payments', verbose_name='Клиент')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Оплата')
    paid_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')

    def __str__(self):
        return f'{self.client} {self.amount} {self.paid_at}'


class Training(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='trainings', verbose_name='Клиент')
    date = models.DateField(auto_now_add=True, verbose_name='Дата проведения тренировки')
    group = models.ForeignKey(Group, blank=True, null=True, on_delete=models.PROTECT, related_name='trainings',
                              verbose_name='Группа')

    def __str__(self):
        return f'{self.client} | {self.date}'
