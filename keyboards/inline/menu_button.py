from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData
from backend.models import *

async def phone_keyboard():
    texts = []
    texts = ["Raqamni ulashish", "Orqaga"]
    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text=f"📞 {texts[0]}", request_contact=True)
    key2 = KeyboardButton(text=f"⬅️ {texts[1]}")
    keyboard.add(key1)
    keyboard.resize_keyboard = True
    return keyboard


async def main_keyboard():
    texts = ["Konkurs haqida", "Xafta g'oliblari"]
    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text=f"{texts[0]}")
    key2 = KeyboardButton(text=f"{texts[1]}")
    keyboard.add(key1, key2)
    keyboard.resize_keyboard = True
    return keyboard
    
