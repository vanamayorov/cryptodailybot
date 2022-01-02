from datetime import date
import json
import os
import sqlite3
from aiogram.types import Message


def get_date():
    return date.today().strftime("%d/%m/%Y")


def to_fixed(num_obj, digits=0):
    return f"{num_obj:.{digits}f}"


def get_market_type():
    path = "additional_info.json"
    if not os.path.exists(path):
        raise FileNotFoundError

    with open(path, 'r') as f:
        content = json.load(f)

    return content['typeOfMarket']


def define_change(number):
    if float(number) > 0:
        return f'+{number}% 🟢'
    return f'{number}% 🔴'


def check_user_in_db(message: Message):
    chat_id = message.chat.id

    with sqlite3.connect('db/mybot_db.db') as db:
        cursor = db.cursor()
        cursor.execute(f"SELECT * from users WHERE chat_id={chat_id}")
        data = cursor.fetchone()

    if not data:
        return False
    return True
