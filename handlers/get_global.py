from aiogram.types import Message
from loader import dp
from bs4 import BeautifulSoup
import requests
from functions.custom_functions import get_market_type, to_fixed, get_date
from data.links import COINMARKETCAP_URL, ALTCOINSEASON_URL
from pycoingecko import CoinGeckoAPI
from aiogram.dispatcher.filters import Text

cg = CoinGeckoAPI()


def get_global_info():
    r = requests.get(COINMARKETCAP_URL)
    soup = BeautifulSoup(r.text, 'lxml')
    market_cap = soup.find('div', {"class": "cmc-header-desktop"}).find('div', {"class": "container"}).find('div') \
        .find_all('a', {'class': 'cmc-link'})[2].text
    btc_dom = to_fixed(cg.get_global()['market_cap_percentage']['btc'], 1)
    alt_dom = to_fixed(100 - cg.get_global()['market_cap_percentage']['btc'], 1)
    num_of_crypto = soup.find('div', {"class": "cmc-header-desktop"}).find('div', {"class": "container"}).find('div') \
        .find_all('a', {'class': 'cmc-link'})[0].text
    day_volume = soup.find('div', {"class": "cmc-header-desktop"}).find('div', {"class": "container"}).find('div') \
        .find_all('a', {'class': 'cmc-link'})[3].text
    r = requests.get(ALTCOINSEASON_URL)
    soup = BeautifulSoup(r.text, 'lxml')
    altcoinseason = soup.find("div", {"class": "altseasoncontent"}).find("div", {"class": "m-3"}).text
    output = f'Date: {get_date()} \nMarket cap: {market_cap}\nBTC Dominance: {btc_dom}\nALT Dominance: {alt_dom}\n' \
             f'Type of market: {get_market_type()}\nNum of cryptocurrencies: {num_of_crypto}\n24h Vol: {day_volume}\n' \
             f'Altcoin season: {altcoinseason[0:-2].lower()}'
    return output


@dp.message_handler(Text(equals=["Global📊", "/global"]))
async def get_global(message: Message):
    await message.answer(text=get_global_info())
