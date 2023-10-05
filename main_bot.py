import telebot
import buttons
import database
import openpyxl
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

bot = telebot.TeleBot(os.getenv('KEY'))

# Путь к файлу Excel
excel_file_path = 'user_data.xlsx'

# Путь к файлу для хранения даты последней отправки отчета
last_report_sent_file = 'last_report_sent.txt'


@bot.message_handler(commands=['start'])
def send_number(message):
    user_id = message.from_user.id
    name = message.from_user.username

    if message.contact:
        phone_number = message.contact.phone_number

        # Сохраняем пользователя в Excel
        save_user_to_excel(user_id, name, phone_number)

        bot.send_message(user_id, 'Отправьте фото или скриншот товара',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, send_image, name, phone_number)
    elif not message.contact:
        bot.send_message(user_id, 'Отправьте контакт с помощью кнопки', reply_markup=buttons.number_buttons())
        bot.register_next_step_handler(message, send_number)


def send_image(message, name, phone_number):
    user_id = message.from_user.id
    if message.photo:
        photo = message.photo[-1].file_id
        bot.send_message(user_id, 'Успешно! Ждите ответа от наших операторов')

        # Отправляем информацию в группу
        send_info_to_group(user_id, name, phone_number, photo)


def send_image(message, name, phone_number):
    user_id = message.from_user.id
    if message.photo:
        photo = message.photo[-1].file_id
        bot.send_message(user_id, 'Успешно! Ждите ответа от наших операторов')

        posting = bot.send_photo(-4013840171, photo=photo, caption=f"<b>Имя</b>: {name}\n"
                                                                   f"<b>ID</b>: {user_id}\n"
                                                                   f"<b>Номер телефона</b>: {phone_number}",
                                 parse_mode="html", reply_markup=buttons.promo_call(user_id))


def send_promo(message, user_id, admin_id):
    if message.from_user.id == admin_id:
        try:
            bot.send_message(user_id, message.text)
            bot.send_message(-4013840171, f"{user_id} получил промокод")
        except:
            bot.send_message(-4013840171, f"{user_id} не получил промокод")


@bot.callback_query_handler(func=lambda call: True)
def promo(call):
    user_id = int(call.data)
    admin_id = call.from_user.id
    bot.send_message(-4013840171, f"Отправьте сообщение для юзера с айди: {user_id}")
    bot.register_next_step_handler(call.message, send_promo, user_id, admin_id)


def save_user_to_excel(user_id, username, phone_number):
    if not os.path.exists(excel_file_path):
        # Создаем новый файл Excel и добавляем заголовки
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(['User ID', 'Username', 'Phone Number'])
    else:
        # Открываем существующий файл Excel
        wb = openpyxl.load_workbook(excel_file_path)
        ws = wb.active

    # Добавляем данные пользователя в Excel
    ws.append([user_id, username, phone_number])

    # Получаем максимальную длину имени пользователя
    max_username_length = max(len(row[1].value) for row in ws.iter_rows(min_row=2, max_row=ws.max_row))

    # Устанавливаем ширину столбца "Username" на основе максимальной длины имени
    ws.column_dimensions['B'].width = max_username_length + 2  # Добавляем немного места для отступа

    # Сохраняем файл
    wb.save(excel_file_path)


def send_info_to_group(user_id, username, phone_number, photo):
    bot.send_photo(-4013840171, photo=photo, caption=f"<b>Имя 👤</b>: {username}\n"
                                                     f"<b>ID 🆔</b>: {user_id}\n"
                                                     f"<b>Номер телефона 📞</b>: {phone_number}",
                   parse_mode="html")


def send_excel_report_to_group():
    if os.path.exists(excel_file_path):
        today = datetime.date.today()
        last_modified = datetime.date.fromtimestamp(os.path.getmtime(excel_file_path))

        # Проверяем, был ли файл изменен в последние 30 дней
        if (today - last_modified).days <= 30:
            # Проверяем, отправляли ли отчет сегодня
            if not os.path.exists(last_report_sent_file) or (today - get_last_report_sent_date()).days >= 1:
                bot.send_document(-4013840171, open(excel_file_path, 'rb'))
                save_last_report_sent_date(today)


def get_last_report_sent_date():
    if os.path.exists(last_report_sent_file):
        with open(last_report_sent_file, 'r') as file:
            last_report_date = datetime.datetime.strptime(file.read(), '%Y-%m-%d').date()
            return last_report_date
    else:
        return None


def save_last_report_sent_date(date):
    with open(last_report_sent_file, 'w') as file:
        file.write(date.strftime('%Y-%m-%d'))


# Запуск рассылки отчета каждые 30 дней
send_excel_report_to_group()

# Запуск бота
bot.infinity_polling()
