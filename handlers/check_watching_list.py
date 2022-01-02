from aiogram.types import Message
from loader import dp
from aiogram.dispatcher.filters import Text
from aiogram import types
import sqlite3
import keyboards
from pycoingecko import CoinGeckoAPI
from functions.custom_functions import define_change, to_fixed, check_user_in_db

cg = CoinGeckoAPI()


@dp.message_handler(Text(equals=["Check my watching list🔄", "/check_list"]))
async def check_list(message: Message):
    if not check_user_in_db(message):
        await message.answer("You are not logged in, please create your personal portfolio account.",
                             reply_markup=keyboards.StartKeyboard.keyboard)
        return None

    chat_id = message.chat.id

    with sqlite3.connect('db/mybot_db.db') as db:
        cursor = db.cursor()
        cursor.execute(f"SELECT crypto_name from watching_list WHERE chat_id={chat_id}")
        data = cursor.fetchall()

    if not data:
        await message.answer("Your watching list📋 is empty, please add any coin.",
                             reply_markup=keyboards.PersonalPortfolioKeyboard.keyboard)
    else:
        result_string = ''

        for crypto in data:
            crypto_name = " ".join(crypto[0].split("-"))
            result_string += f'[{crypto_name.capitalize()}]:\n${cg.get_price(ids=crypto[0], vs_currencies="usd")[crypto[0]]["usd"]} {define_change(to_fixed(cg.get_price(ids=crypto[0], vs_currencies="usd", include_24hr_change="true")[crypto[0]]["usd_24h_change"], 2))}' + '\n'

        await message.answer(f"<b>Your watching list📋:</b>\n<code>{result_string}</code>",
                             reply_markup=keyboards.PersonalPortfolioKeyboard.keyboard)
