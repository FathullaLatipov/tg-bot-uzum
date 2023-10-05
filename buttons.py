from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def number_buttons():
    # Создать пространство для кнопок
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)

    num_button = types.KeyboardButton('Поделиться контактом', request_contact=True)

    buttons.add(num_button)

    return buttons


def promo_call(user_id):
    kb = InlineKeyboardMarkup(row_width=1)
    mm = InlineKeyboardButton(text="Ответить", callback_data=f"{user_id}")
    kb.row(mm)
    return kb