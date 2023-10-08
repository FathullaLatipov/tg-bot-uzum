from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def promokod():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Получить промокод')
    kb.add(button)
    return kb
def promokod_uz():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Promo-kodni olish')
    kb.add(button)
    return kb
def cancel_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    one = KeyboardButton("❌Отмена")
    kb.add(one)
    return kb
def promo_call(user_id):
    kb = InlineKeyboardMarkup(row_width=1)
    mm = InlineKeyboardButton(text="Ответить", callback_data=f"{user_id}")
    kb.row(mm)
    return kb
def language_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    rus = KeyboardButton("Русский язык")
    uzb = KeyboardButton("O'zbek tili")
    kb.add(rus, uzb)
    return kb


def promo_call(user_id):
    kb = InlineKeyboardMarkup(row_width=1)
    mm = InlineKeyboardButton(text="Ответить", callback_data=f"{user_id}")
    kb.row(mm)
    return kb