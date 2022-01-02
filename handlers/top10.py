from aiogram.types import Message,  CallbackQuery
from loader import dp
from functions.custom_functions import to_fixed, define_change
from aiogram.dispatcher.filters import Text
from pycoingecko import CoinGeckoAPI
import keyboards

cg = CoinGeckoAPI()


def get_top10_info():
    top10_list = []
    for item in cg.get_coins_markets(vs_currency="usd", per_page=10, page=1, price_change_percentage="24h"):
        top10_list.append(
            {"name": item["name"], "price": item["current_price"], "change": item["price_change_percentage_24h"]})
    output = '<b>Top 10 coins over 24h:🗓️</b>\n'
    for coin in top10_list:
        output += f'<code>{coin["name"]}: {to_fixed(float(coin["price"]), 2)}$\n[change 24h]: {define_change(to_fixed(coin["change"], 2))}</code>\n'
    return output


@dp.message_handler(Text(equals=["Top10📈", "/top10"]))
async def get_top10(message: Message):
    await message.answer(text=get_top10_info(), parse_mode="HTML", reply_markup=keyboards.InlineKeyboard.keyboard)


@dp.callback_query_handler(text="refresh")
async def refresh_data(call: CallbackQuery):
    await call.message.edit_text(text=get_top10_info(),
                                 parse_mode="HTML", reply_markup=keyboards.InlineKeyboard.keyboard)
