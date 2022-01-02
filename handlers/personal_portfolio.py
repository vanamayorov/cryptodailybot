from aiogram.types import Message
from loader import dp
import sqlite3
from aiogram.dispatcher.filters import Text
import keyboards


@dp.message_handler(Text(equals=["Personal Portfolio💼", "/personal_portfolio"]))
async def portfolio_login(message: Message):
    chat_id = message.chat.id
    with sqlite3.connect('db/mybot_db.db') as db:
        cursor = db.cursor()
        cursor.execute(f"SELECT chat_id from users WHERE chat_id={chat_id}")
        data = cursor.fetchone()
        if data is None:
            cursor.execute(f""" INSERT INTO users(id, chat_id) VALUES (NULL, {chat_id}) """)
    await message.answer(
        text="You have logged in to your personal portfolio, now some extra commands are available to you.\n"
             "Commands:\n"
             "/awl &lt;coin&gt;: Adds coin to your watching list. You can add a couple of cryptos at once"
             "separated by commas or one by one using this command\n"
             "/rwl &lt;coin&gt;: Removes coin from your watching list. You can remove a couple of coins"
             "at once separated by commas or one by one using this command\n"
             "/check_list: Returns actual data about coins in your watching list\n"
             "/balance: Returns actual data about coins on your balance\n"
             "/ab &lt;coin&gt; &lt;amount&gt;: Adds coin with some amount to your balance.\n"
             "/rb &lt;coin&gt; &lt;amount&gt;: Removes coin with some amount from your watching list.\n\n\n"
             "Examples:\n"
             "/awl(by default, bitcoin);\n/awl bitcoin, ethereum, ripple\n"
             "/rwl(by default, bitcoin);\n/rwl bitcoin, ethereum, ripple\n"
             "/ab(by default, bitcoin 1);\n/ab ethereum 5\n"
             "/rb(by default, bitcoin 1);\n/rb ethereum 5\n",
        reply_markup=keyboards.PersonalPortfolioKeyboard.keyboard)


@dp.message_handler(Text(equals=["Log out from a personal portfolio🔙", "/logout"]))
async def portfolio_logout(message: Message):
    await message.answer(text="You have logged out from a personal portfolio!",
                         reply_markup=keyboards.StartKeyboard.keyboard)
