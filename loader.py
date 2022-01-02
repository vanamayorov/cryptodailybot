import asyncio
from data.config import token
from aiogram import Bot, Dispatcher
from aiogram import types


loop = asyncio.get_event_loop()
bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, loop=loop)