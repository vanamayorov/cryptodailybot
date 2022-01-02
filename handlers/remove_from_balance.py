from aiogram.types import Message
from loader import dp
from aiogram.dispatcher.filters import Text
from aiogram import types
import sqlite3
import keyboards
from pycoingecko import CoinGeckoAPI
from functions.custom_functions import check_user_in_db

cg = CoinGeckoAPI()


@dp.message_handler(commands=['rb'])
async def remove_from_balance(message: Message):
    try:
        if not check_user_in_db(message):
            await message.answer("You are not logged in, please create your personal portfolio account.",
                                 reply_markup=keyboards.StartKeyboard.keyboard)
            return None

        chat_id = message.chat.id
        if not message.text[len('rb ')::].lower().strip():
            crypto_name = 'bitcoin'
            crypto_amount = 1
        else:
            crypto_amount = "".join(filter(str.isdigit, message.text[len('rb ')::]))
            if not crypto_amount:
                await message.answer("Invalid type of amount, try again.",
                                     reply_markup=keyboards.PersonalPortfolioKeyboard.keyboard)
                return None
            crypto_name = "-".join(message.text[len('rb '):-len(crypto_amount)].lower().strip().split(' '))

            if not cg.get_price(ids=crypto_name, vs_currencies="usd"):
                await message.answer(f"{crypto_name.capitalize()} was not found, try again.",
                                     reply_markup=keyboards.PersonalPortfolioKeyboard.keyboard)
                return None

        with sqlite3.connect('db/mybot_db.db') as db:
            cursor = db.cursor()
            cursor.execute(f"""SELECT chat_id from balance WHERE chat_id={chat_id}""")
            data = cursor.fetchone()

            if not data:
                await message.answer("Your balance is empty. There is nothing to remove",
                                     reply_markup=keyboards.PersonalPortfolioKeyboard.keyboard)
            else:
                cursor.execute(""" SELECT amount FROM balance WHERE chat_id=? AND crypto_name=? """,
                               (chat_id, crypto_name))
                data = cursor.fetchone()

                if not data:
                    await message.answer(f"[{crypto_name.capitalize()}] is not in your watching list.",
                                         reply_markup=keyboards.PersonalPortfolioKeyboard.keyboard)
                else:
                    if data[0] - int(crypto_amount) <= 0:
                        cursor.execute("""DELETE FROM balance WHERE chat_id=? AND crypto_name=?""",
                                       (chat_id, crypto_name))

                        await message.answer(
                            f"All coins of [{crypto_name.capitalize()}] have just been removed from your balance",
                            reply_markup=keyboards.PersonalPortfolioKeyboard.keyboard)
                    else:
                        cursor.execute(""" UPDATE balance SET amount=? WHERE chat_id=? AND crypto_name=? """,
                                       (data[0] - int(crypto_amount), chat_id, crypto_name))

                        await message.answer(
                            f"[{crypto_name.capitalize()}] with amount of &lt;{crypto_amount}&gt; has just been removed from your balance",
                            reply_markup=keyboards.PersonalPortfolioKeyboard.keyboard)
    except Exception as e:
        print(e)
