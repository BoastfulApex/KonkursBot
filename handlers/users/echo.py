from loader import dp, bot
from aiogram import types


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer(message.text)
