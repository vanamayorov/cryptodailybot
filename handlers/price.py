from aiogram.types import Message
from loader import dp
from pycoingecko import CoinGeckoAPI
from functions.custom_functions import to_fixed, define_change

cg = CoinGeckoAPI()


@dp.message_handler(commands=['p'])
async def get_coin_price(message: Message):
    if not message.text[2::].lower().strip():
        crypto_name = 'bitcoin'
        value_in_btc = ''
    else:
        crypto_name = "-".join(message.text[2::].lower().strip().split(' '))
        value_in_btc = " | " + str(cg.get_price(ids=crypto_name, vs_currencies="btc")[crypto_name]["btc"]) + '₿'

    try:
        await message.answer(text=
                             f'<code>'
                             f'{crypto_name.capitalize()}:\n${cg.get_price(ids=crypto_name, vs_currencies="usd")[crypto_name]["usd"]}{value_in_btc}\n'
                             f'H|L:  ${to_fixed(cg.get_coins_markets(ids=crypto_name, vs_currency="usd", price_change_percentage="24h")[0]["high_24h"], 2)}|${to_fixed(cg.get_coins_markets(ids=crypto_name, vs_currency="usd", price_change_percentage="24h")[0]["low_24h"], 2)}\n'
                             f'1h      {define_change(to_fixed(cg.get_coins_markets(ids=crypto_name, vs_currency="usd", price_change_percentage="1h")[0]["price_change_percentage_1h_in_currency"], 2))}\n'
                             f'24h     {define_change(to_fixed(cg.get_coins_markets(ids=crypto_name, vs_currency="usd", price_change_percentage="24h")[0]["price_change_percentage_24h_in_currency"], 2))}\n'
                             f'7d      {define_change(to_fixed(cg.get_coins_markets(ids=crypto_name, vs_currency="usd", price_change_percentage="7d")[0]["price_change_percentage_7d_in_currency"], 2))}\n'
                             f'</code>')
    except KeyError:
        await message.answer(text=
                             f'The current Price not found for {crypto_name}')
