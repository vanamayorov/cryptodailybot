from aiogram.types import Message
from loader import dp
import keyboards


@dp.message_handler(commands=['start', 'help'])
async def start_message(message: Message):
    await message.answer(text="CryptoDailyBot\n"
                              "Commands:⬇️\n"
                              "/global: Returns daily information about crypto market📊\n"
                              "/p &lt;coin&gt;: Returns the current &lt;coin&gt; price in $💵\n"
                              "/top10: Returns top10 coins by capitalization📈\n"
                              "/personal_portfolio: Login to your personal cabinet💼\n\n\n"
                              "Examples:\n"
                              "/p bitcoin; /p ethereum; /p(by default, bitcoin)\n",
                         reply_markup=keyboards.StartKeyboard.keyboard)
