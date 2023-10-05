import sqlite3
from datetime import datetime
connection = sqlite3.connect("qr_bot.db")
sql = connection.cursor()
sql.execute("CREATE TABLE IF NOT EXISTS all_users (tg_id INTEGER, name TEXT, phone_number TEXT, reg_date DATETIME);")
connection.commit()

def reg_user(user_id, name, phone_number):
    connection = sqlite3.connect("qr_bot.db")
    sql = connection.cursor()
    sql.execute("INSERT INTO all_users (tg_id, name, phone_number, reg_date) "
                "VALUES (?, ?, ?, ?);", (user_id, name, phone_number, datetime.now()))
    connection.commit()

def get_all_users():
    connection = sqlite3.connect("qr_bot.db")
    sql = connection.cursor()
    all_users = sql.execute("SELECT * FROM all_users;").fetchall()
    return all_users