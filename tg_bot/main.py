import os
import logging
from typing import List
import aiohttp
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery
from aiogram.utils import executor
from keyboards import kb, admin_kb, get_group_kb, invite_button
from validators import is_valid_link
import datetime
import redis
from aiogram import exceptions as aiogram_exceptions
from fsm import StartTrainingState
from aiogram.contrib.fsm_storage.memory import MemoryStorage

pool = redis.ConnectionPool(host='redis', port=6379, db=1)
redis = redis.Redis(connection_pool=pool)

TOKEN = os.environ.get('BOT_TOKEN')
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
admin: int = int(os.environ.get('ADMIN'))


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.from_user.id == admin:
        await message.answer(text='Добро пожаловать!', reply_markup=admin_kb)
    else:
        await message.answer(text='Добро пожаловать!', reply_markup=kb)


@dp.message_handler(Text('Регистрация'))
async def register_user(message: types.Message):
    user_id: str = str(message.from_user.id)
    url: str = f"{os.environ.get('CLIENT_CHECK_API')}{user_id}"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    result: str = (await response.json())['result']
                    if result == 'client':
                        await message.answer('Вы уже зарегистрированы как клиент')
                    elif result == 'coach':
                        await message.answer('Вы уже зарегистрированы как тренер')
                elif response.status == 404:
                    data: dict = {'telegram_name': user_id}
                    async with session.post(os.environ.get('CLIENT_CREATE_API'), data=data) as response:
                        if response.status == 201:
                            await message.answer('Вы успешно зарегистрированы как клиент')
                        else:
                            await message.answer('Произошла ошибка при регистрации')
                else:
                    await message.answer('Произошла ошибка при проверке наличия пользователя в базе данных')
                    raise Exception('Произошла ошибка при проверке наличия пользователя в базе данных')
        except aiohttp.ClientResponseError as e:
            await message.answer(f'Произошла ошибка при выполнении запроса: {e.status}')
        except aiohttp.ClientError as e:
            await message.answer(f'Произошла ошибка сети: {e}')
            logger.exception(e)


async def get_groups():
    url: str = f"{os.environ.get('GET_GROUP_LIST_API')}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                groups = (await response.json())
                return groups


async def get_active_clients_in_group(group_id):
    url: str = f"{os.environ.get('GET_CLIENTS_IN_GROUP_API')}{group_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                clients = (await response.json())
                return clients


@dp.message_handler(lambda message: not is_valid_link(message.text), state=StartTrainingState.link)
async def link_invalid(message: types.Message, state: FSMContext):
    if message.text.lower().replace('/', '') == 'cancel':
        await state.finish()
        await message.reply('Операция отменена.')
        return
    return await message.reply("Некорректная ссылка, попробуйте еще раз.")


@dp.message_handler(state=StartTrainingState.link)
async def get_link(message: types.Message, state: FSMContext):
    link: str = message.text
    await state.update_data(link=link)
    redis.set('google_link', link)
    if message.from_user.id == admin:
        data = await state.get_data()
        group_id = data['group']
        clients = await get_active_clients_in_group(group_id)
        client_list = []
        for client in clients:
            client_list.append(client['telegram_name'])
        await StartTrainingState.send_invite.set()
        await send_invite_buttons_to_clients(client_list, state)


@dp.callback_query_handler(lambda c: c.data.startswith('invite_'))
async def invite_callback(callback_query: CallbackQuery):
    user_id: int = callback_query.from_user.id
    url: str = os.environ.get('TRAINING_CREATE_API')
    data: dict = {'telegram_name': user_id}
    callback_data = callback_query.data.split('_')
    telegram_name = callback_data[1]
    expiration_text = callback_data[2]
    expiration_time = datetime.datetime.strptime(expiration_text, '%Y-%m-%d %H:%M:%S')
    if datetime.datetime.now() < expiration_time:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=data) as response:
                    if response.status == 201:
                        await bot.send_message(callback_query.from_user.id, text='Тренировка создана!')
                        django_link = redis.get('google_link').decode('utf-8')
                        await bot.send_message(callback_query.from_user.id, text=f'Ссылка на занятие: {django_link}')
                        await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                                             message_id=callback_query.message.message_id, reply_markup=None)
                    else:
                        await bot.send_message(callback_query.from_user.id, text='Не удалось создать тренировку!')
        except aiohttp.ClientError as e:
            logger.exception(e)
            await bot.send_message(callback_query.from_user.id, text=f'Ошибка: {str(e)}')
        except Exception as e:
            logger.exception(e)
            await bot.send_message(callback_query.from_user.id, text=f"Error sending invite to {telegram_name}: {e}")
    else:
        await bot.answer_callback_query(callback_query.id, text="Приглашение не активно!")
    await bot.answer_callback_query(callback_query.id)


@dp.message_handler(state=StartTrainingState.send_invite)
async def send_invite_buttons_to_clients(clients: List, state: FSMContext):
    await state.update_data(send_invite=True)
    for client in clients:
        invite_markup = invite_button(client)
        try:
            if redis.get('google_link'):
                await bot.send_message(client, text='Приглашение на тренировку:', reply_markup=invite_markup)
        except aiogram_exceptions.BotBlocked as e:
            logger.exception(f"Ошибка отправки приглашения: {e}")
        except aiogram_exceptions.TelegramAPIError as e:
            logger.exception(f"Ошибка отправки приглашения: {e}")
    await state.finish()


@dp.callback_query_handler(lambda c: c.data.startswith('group_'), state=StartTrainingState.group)
async def group_callback(callback_query: CallbackQuery, state: FSMContext):
    group_id: int = int(callback_query.data.replace('group_', ''))
    clients = await get_active_clients_in_group(group_id)
    if clients:
        await bot.send_message(text="Введите ссылку на занятие:", chat_id=admin)
        await state.update_data(group=group_id)
        await StartTrainingState.link.set()
    else:
        await bot.send_message(callback_query.from_user.id, text='В этой группе нет активных клиентов!')
        await StartTrainingState.group.set()
    await bot.answer_callback_query(callback_query.id)


@dp.message_handler(commands=['cancel'], state='*')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Операция отменена.')


@dp.message_handler(Text('Начать занятие'))
async def start_training(message: types.Message):
    try:
        groups = await get_groups()
        if groups:
            group_list_kb = get_group_kb(groups)
            await message.answer(text='Выберите, пожалуйста, группу:',
                                 reply_markup=group_list_kb)
            await StartTrainingState.group.set()
        else:
            await message.answer('Произошла ошибка при подключении к серверу!')
            raise ConnectionError("Произошла ошибка при подключении к серверу!")
    except ConnectionError as conn_err:
        logger.exception(conn_err)
        await message.answer('Ошибка подключения к серверу!')
    except Exception as e:
        logger.exception(e)

        await message.answer('Произошла ошибка при выполнении команды!')


@dp.message_handler(commands=['massmailing'])
async def massmailing(message: types.Message):
    url = os.environ.get('MASS_MAILING_API')

    try:
        text: str = message.text.replace('/massmailing', '')

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    users: list = await response.json()
                    for user in users:
                        if user['telegram_name']:
                            try:
                                await bot.send_message(user['telegram_name'], text)
                            except Exception as e:
                                error_message = f"Не удалось отправить сообщение пользователю {user['telegram_name']}. Ошибка: {e}"
                                logger.exception(error_message)
                                await bot.send_message(message.from_user.id, error_message)
                    await bot.send_message(message.from_user.id, 'Сообщение успешно отправлено')
                else:
                    error_message = 'Ошибка при запросе к API'
                    logger.exception(error_message)
                    await bot.send_message(message.from_user.id, error_message)
                    raise ConnectionError(error_message)
    except (ValueError, ConnectionError) as err:
        logger.exception(err)
        await bot.send_message(message.from_user.id, f"Произошла ошибка: {err}")
    except Exception as e:
        logger.exception(e)
        await bot.send_message(message.from_user.id, 'Произошла ошибка при выполнении команды')


@dp.message_handler(commands=['sendallactiveclients'])
async def sendallactiveclients(message: types.Message):
    url = os.environ.get('SEND_ALL_ACTIVE_CLIENTS_API')

    try:
        text: str = message.text.replace('/sendallactiveclients', '')

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    users: list = await response.json()
                    for user in users:
                        if user['telegram_name']:
                            try:
                                await bot.send_message(user['telegram_name'], text)
                            except Exception as e:
                                error_message = f"Не удалось отправить сообщение пользователю {user['telegram_name']}. Ошибка: {e}"
                                logger.exception(error_message)
                                await bot.send_message(message.from_user.id, error_message)
                    await bot.send_message(message.from_user.id, 'Сообщение успешно отправлено')
                else:
                    error_message = 'Ошибка при запросе к API'
                    logger.exception(error_message)
                    await bot.send_message(message.from_user.id, error_message)
                    raise ConnectionError(error_message)
    except (ValueError, ConnectionError) as err:
        logger.exception(err)
        await bot.send_message(message.from_user.id, f"Произошла ошибка: {err}")
    except Exception as e:
        logger.exception(e)
        await bot.send_message(message.from_user.id, 'Произошла ошибка при выполнении команды')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)