from aiogram.types import Message
from loader import dp
from aiogram.dispatcher.filters import Text
from aiogram import types
import sqlite3
import keyboards
from pycoingecko import CoinGeckoAPI
from functions.custom_functions import check_user_in_db

cg = CoinGeckoAPI()


@dp.message_handler(commands=['ab'])
async def add_to_balance(message: Message):
    if not check_user_in_db(message):
        await message.answer("You are not logged in, please create your personal portfolio account.",
                             reply_markup=keyboards.StartKeyboard.keyboard)
        return None

    chat_id = message.chat.id

    if not message.text[len('ab ')::].lower().strip():
        crypto_name = "bitcoin"
        crypto_amount = 1
    else:
        crypto_amount = "".join(filter(str.isdigit, message.text[len('ab ')::]))
        if not crypto_amount:
            await message.answer("Invalid type of amount, try again.",
                                 reply_markup=keyboards.PersonalPortfolioKeyboard.keyboard)
            return None
        crypto_name = "-".join(message.text[len('atb '):-len(crypto_amount)].lower().strip().split(' '))

        if not cg.get_price(ids=crypto_name, vs_currencies="usd"):
            await message.answer(f"{crypto_name.capitalize()} was not found, try again.",
                                 reply_markup=keyboards.PersonalPortfolioKeyboard.keyboard)
            return None

    with sqlite3.connect('db/mybot_db.db') as db:
        cursor = db.cursor()
        cursor.execute(f"SELECT chat_id from balance WHERE chat_id={chat_id}")
        data = cursor.fetchone()

        if not data:
            cursor.execute(
                f""" INSERT INTO balance(id, chat_id, crypto_name, amount) VALUES (NULL, ?, ?, ?) """,
                (chat_id, crypto_name, crypto_amount))
            crypto_name = " ".join(crypto_name.split("-"))
            await message.answer(
                f"[{crypto_name.capitalize()}] with amount of &lt;{crypto_amount}&gt; has just been added to your balance",
                reply_markup=keyboards.PersonalPortfolioKeyboard.keyboard)
        else:
            cursor.execute(f""" SELECT * FROM balance WHERE chat_id=? AND crypto_name=? """, (chat_id, crypto_name))
            data = cursor.fetchone()

            if not data:
                cursor.execute(
                    f""" INSERT INTO balance(id, chat_id, crypto_name, amount) VALUES (NULL, ?, ?, ?) """,
                    (chat_id, crypto_name, crypto_amount))
                crypto_name = " ".join(crypto_name.split("-"))
                await message.answer(
                    f"[{crypto_name.capitalize()}] with amount of &lt;{crypto_amount}&gt; has just been added to your balance",
                    reply_markup=keyboards.PersonalPortfolioKeyboard.keyboard)
            else:
                cursor.execute(f""" UPDATE balance SET amount=? WHERE crypto_name=? """, (crypto_amount, crypto_name))
                await message.answer(
                    f"[{crypto_name.capitalize()}] with amount of &lt;{crypto_amount}&gt; has just been updated in your balance",
                    reply_markup=keyboards.PersonalPortfolioKeyboard.keyboard)
