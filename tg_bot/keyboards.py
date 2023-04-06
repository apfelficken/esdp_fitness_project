from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import datetime

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Регистрация')
kb.add(button1)

admin_kb = ReplyKeyboardMarkup(resize_keyboard=True)
button2 = KeyboardButton(text='Начать занятие')
admin_kb.add(button2)


def get_group_kb(groups):
    group_kb = InlineKeyboardMarkup(row_width=1)
    for group in groups:
        group_kb.add(InlineKeyboardButton(group['name'], callback_data=f"group_{group['id']}"))
    return group_kb


def invite_button(telegram_name: str) -> InlineKeyboardMarkup:
    expiration_time = datetime.datetime.now() + datetime.timedelta(seconds=30)
    expiration_text = expiration_time.strftime('%Y-%m-%d %H:%M:%S')
    button = InlineKeyboardButton(
        text="Присоединиться к тренировке",
        callback_data=f"invite_{telegram_name}_{expiration_text}"
    )
    markup = InlineKeyboardMarkup()
    markup.add(button)
    return markup
