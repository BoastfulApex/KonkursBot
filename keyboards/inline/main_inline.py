from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData
from backend.models import *
from utils.db_api.database import *


async def channels_keyboard(channels):
    markup = InlineKeyboardMarkup(row_width=1)
    for i in channels:
        markup.insert(InlineKeyboardButton(text=f"➕ {i.name}", url=i.link))
    markup.insert(InlineKeyboardButton(text=f"✅ A'zo bo'ldim", callback_data="Done"))
    return markup



message_id = 123456789  # The ID of the message sent by the bot
forward_text = "Forward this message"
async def forward_keyboard():
    forward_button = InlineKeyboardButton(text=forward_text, switch_inline_query=f"\n\nforward {message_id}")
    keyboard = InlineKeyboardMarkup().add(forward_button)
    return keyboard