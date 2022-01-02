from aiogram.types import Message
from loader import dp
from aiogram.dispatcher.filters import Text
from aiogram import types
import sqlite3
import keyboards
from pycoingecko import CoinGeckoAPI
from functions.custom_functions import check_user_in_db

cg = CoinGeckoAPI()


@dp.message_handler(commands=['awl'])
async def add_to_watching_list(message: Message):
    if not check_user_in_db(message):
        await message.answer("You are not logged in, please create your personal portfolio account.",
                             reply_markup=keyboards.StartKeyboard.keyboard)
        return None

    chat_id = message.chat.id
    if not message.text[len('awl ')::].lower().strip():
        crypto_name = "bitcoin"
    else:
        crypto_name = "-".join(message.text[len('awl ')::].lower().strip().split(' '))

    if cg.get_price(ids=crypto_name, vs_currencies="usd"):
        with sqlite3.connect('db/mybot_db.db') as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT chat_id from watching_list WHERE chat_id={chat_id}")
            data = cursor.fetchone()
            if not data:
                cursor.execute(
                    f""" INSERT INTO watching_list(id, chat_id, crypto_name) VALUES (NULL, ?, ?) """,
                    (chat_id, crypto_name))
                crypto_name = " ".join(crypto_name.split("-"))
                await message.answer(f"{crypto_name.capitalize()} has just been added to your watching list",
                                     reply_markup=keyboards.PersonalPortfolioKeyboard.keyboard)
            else:
                cursor.execute(
                    "SELECT crypto_name from watching_list WHERE chat_id=? AND crypto_name=?", (chat_id, crypto_name))
                data = cursor.fetchone()
                if not data:
                    cursor.execute(
                        f""" INSERT INTO watching_list(id, chat_id, crypto_name) VALUES(NULL, ?, ?) """,
                        (chat_id, crypto_name))
                    crypto_name = " ".join(crypto_name.split("-"))
                    await message.answer(f"{crypto_name.capitalize()} has just been added to your watching list",
                                         reply_markup=keyboards.PersonalPortfolioKeyboard.keyboard)
                else:
                    crypto_name = " ".join(crypto_name.split("-"))
                    await message.answer(f"{crypto_name.capitalize()} is already in your watching list",
                                         reply_markup=keyboards.PersonalPortfolioKeyboard.keyboard)
    else:
        crypto_name = " ".join(crypto_name.split("-"))
        await message.answer(f"{crypto_name.capitalize()} was not found, try again.",
                             reply_markup=keyboards.PersonalPortfolioKeyboard.keyboard)
