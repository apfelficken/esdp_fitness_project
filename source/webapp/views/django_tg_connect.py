import logging
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from webapp.models import Group, Client
from webapp.forms import InviteForm, MailingForm, GroupMailingForm
from django.contrib import messages
from typing import List
import requests
import asyncio
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime
from aiogram.dispatcher import Dispatcher
import redis
from aiogram import exceptions as aiogram_exceptions
import os

pool = redis.ConnectionPool(host='redis', port=6379, db=1)
redis = redis.Redis(connection_pool=pool)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
TOKEN = os.environ.get('BOT_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


class TelegramDriver:

    def __init__(self):
        pass

    def invite_button(self, telegram_name) -> InlineKeyboardMarkup:
        expiration_time = datetime.datetime.now() + datetime.timedelta(seconds=30)
        expiration_text = expiration_time.strftime('%Y-%m-%d %H:%M:%S')
        button = InlineKeyboardButton(
            text="Присоединиться к тренировке",
            callback_data=f"invite_{telegram_name}_{expiration_text}"
        )
        markup = InlineKeyboardMarkup()
        markup.add(button)
        return markup

    async def send_invite_buttons_to_client(self, client: str):
        invite_markup = TelegramDriver.invite_button(self, telegram_name=client)
        try:
            await bot.send_message(client, text='Приглашение на тренировку:', reply_markup=invite_markup)
        except aiogram_exceptions.BotBlocked as e:
            logger.exception(f"Ошибка отправки приглашения: {e}")
        except aiogram_exceptions.TelegramAPIError as e:
            logger.exception(f"Ошибка отправки приглашения: {e}")


class SendInvite(View):
    def post(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        active_clients: List = Client.objects.active_clients().filter(group=group)
        form = InviteForm(request.POST)
        if form.is_valid():
            django_link = form.cleaned_data['link']
            redis.set('google_link', django_link)
            for client in active_clients:
                asyncio.run(TelegramDriver.send_invite_buttons_to_client(self, client))
            messages.success(request, 'Приглашение успешно отправлено!', extra_tags='alert alert-success')
        else:
            messages.error(request, 'Ошибка отправки приглашения!', extra_tags='alert alert-danger')
        return redirect('webapp:group_detail', pk=group.pk)


class GroupMailing(View):

    def post(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        clients = Client.objects.all().filter(group=group)
        form = GroupMailingForm(request.POST)
        if form.is_valid():
            sent_clients = []
            unsent_clients = []
            message = form.cleaned_data['message']
            for client in clients:
                chat_id = client.telegram_name
                if chat_id:
                    group_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
                    response = requests.get(group_url)
                    if response.status_code == 200:
                        sent_clients.append(client)
                    else:
                        unsent_clients.append(client)
            if sent_clients:
                message_sent = f"Рассылка отправлена следующим клиентам: {', '.join([client.telegram_name for client in sent_clients])}"
                messages.success(request, message_sent, extra_tags='alert alert-success')
            if unsent_clients:
                message_unsent = f"Следующие клиенты не получили сообщение: {', '.join([client.telegram_name for client in unsent_clients])}"
                messages.warning(request, message_unsent, extra_tags='alert alert-warning')
            if not clients:
                messages.warning(request, 'Нет клиентов в базе данных', extra_tags='alert alert-warning')
            elif not sent_clients and not unsent_clients:
                messages.warning(request, 'Нет клиентов с telegram_name', extra_tags='alert alert-warning')
        else:
            messages.error(request, 'Ошибка. Форма неверна!', extra_tags='alert alert-danger')
        return redirect('webapp:group_detail', pk=group.pk)


class Mailing(View):
    template_name: str = 'django_tg_connect/mailing_page.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'form': MailingForm})

    def post(self, request, *args, **kwargs):
        if request.POST['button_send'] == 'send_to_active_clients':
            clients = Client.objects.active_clients().exclude(is_active=False)
        elif request.POST['button_send'] == 'send_to_all_clients':
            clients = Client.objects.all().exclude(is_active=False)
        form = MailingForm(request.POST)
        if form.is_valid():
            message = request.POST.get('message')
            sent_clients = []
            unsent_clients = []
            for client in clients:
                chat_id = client.telegram_name
                if chat_id:
                    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
                    response = requests.get(url)
                    if response.status_code == 200:
                        sent_clients.append(client)
                    else:
                        unsent_clients.append(client)
            if sent_clients:
                message_sent = f"Рассылка отправлена следующим клиентам: {', '.join([client.telegram_name for client in sent_clients])}"
                messages.success(request, message_sent, extra_tags='alert alert-success')
            if unsent_clients:
                message_unsent = f"Следующие клиенты не получили сообщение: {', '.join([client.telegram_name for client in unsent_clients])}"
                messages.warning(request, message_unsent, extra_tags='alert alert-warning')
            if not sent_clients and not unsent_clients:
                messages.warning(request, 'Нет клиентов в базе данных', extra_tags='alert alert-warning')
        else:
            messages.error(request, 'Ошибка Рассылка не отправлена!', extra_tags='alert alert-danger')
        return redirect('webapp:mailing_page')
