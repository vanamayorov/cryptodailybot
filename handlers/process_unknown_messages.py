from aiogram.types import Message
from loader import dp
from aiogram.dispatcher.filters import Text


@dp.message_handler()
async def process_unknown_messages(message: Message):
    await message.answer(f"{message.text} is unknown command, try again")