import datetime
from aiogram.types import ReplyKeyboardRemove
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from keyboards.inline.menu_button import *
from keyboards.inline.main_inline import *
from utils.db_api.database import *
from django.core.files.base import ContentFile
import random
import pandas as pd
from aiogram.dispatcher.filters.builtin import CommandStart
import re

def isValid(s):
    Pattern = re.compile("(0|91)?[7-9][0-9]{9}")
    return Pattern.match(s)

async def check_chat_member(user_id):
    channels = await get_channels()
    answer = []
    for channel in channels:  
        chat_member = await bot.get_chat_member(chat_id=channel.channel_id, user_id=user_id)
        if chat_member.status == types.ChatMemberStatus.OWNER or chat_member.status == types.ChatMemberStatus.MEMBER:
            pass
        else:
            answer.append(channel)
    return answer


def check_date():
    now = datetime.datetime.now()
    if now.weekday() == 3 and  now.hour == 20:
        return True
    else:
        return False

@dp.channel_post_handler(lambda message: message.text in ['SendPostNotification'], state='*')
async def send_zikr(message: types.Message, state: FSMContext):
    if check_date():
        users = await get_users()
        winners = random.sample(users, 3)
        wins = add_week_winners(winners)
        # try:
        #     text = 'f"10 marotaba'
        #     if zikr.zikr_arabic:
        #         text +=f"\n\n <b>{zikr.zikr_arabic}</b> "
        #     text += f"\n\n <k>{zikr.zikr}</k> "

        #     if zikr.zikr_mean:
        #         text += f"\n\n <k>{zikr.zikr_mean}</k> "
        #     await bot.send_message(chat_id=i.user_id, text=f"10 marotaba\n\n <b>{zikr}</b> \n\n takrorlang")
        # except:
        #     continue
        text = 'Ushbu xafta g\'oliblari: \n'
        i = 1
        for user in wins:
            text += "{i}){user.username}| {user.phone}| {user.name}"
        await bot.send_message(chat_id=1430047107, text=text)


@dp.message_handler(CommandStart(), state='*')
async def start_func(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    user.username = message.from_user.username
    user.save()
    channels = await check_chat_member(message.from_id)
    if channels == []:
        if not user.phone:
            keyboard = await phone_keyboard()
            await message.answer("Tanlovda ishtirok etish uchun telefon raqamingizni xalqaro formatda <b>998YYXXXXXXX</b> kabi kiriting. Yoki raqamni ulashing 👇", reply_markup=keyboard)
            await state.set_state("get_phone")
        elif not user.name:
            await message.answer("Ismingizni kiriting ")
            await state.set_state("get_name")
        else:
            # keyboard = forward_keyboard()
            keyboard = await main_keyboard()
            await message.answer(text=f"Siz konkursda muvaffaqqiyatli a’zo bo’ldingiz", reply_markup=keyboard )
            await state.set_state("main")            
    else:
        markup = await channels_keyboard(channels)
        await message.answer("Konkursda ishtirok etish uchun quyidagi kanallarga a'zo bolishingiz kerak 👇", reply_markup=markup)
        await state.set_state('channel')


@dp.callback_query_handler(state='channel')
async def check_channel(call: types.CallbackQuery, state: FSMContext):
    user = await get_user(call.from_user.id)
    channels = await check_chat_member(call.from_user.id)
    if channels == []:
        await call.message.delete()
        if not user.phone:
            markup = await phone_keyboard()
            await bot.send_message(chat_id=call.from_user.id, text="Telefon raqamininfizni xalqaro formatda <b>998YYXXXXXXX</b> kabi kiriting. Yoki raqamni ulashing 👇", reply_markup=markup)
            await state.set_state("get_phone")
        elif not user.name:
            bot.send_message(chat_id=call.from_user.id, text="Ismingizni kiriting 👇")
            await state.set_state("get_name")
    else:
        markup = await channels_keyboard(channels)
        await call.message.edit_text("Konkursda ishtirok etish uchun quyidagi kanallarga a'zo bolishingiz kerak", reply_markup=markup)
        await state.set_state('channel')


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state="get_phone")
async def get_phone(message: types.Message, state: FSMContext):
    if message.contact:
        phone = message.contact.phone_number[0:]
        user = await get_user(message.from_user.id)
        user.phone = phone
        user.save()
        await message.answer(text=f"Ismingizni kiriting 👇", reply_markup=ReplyKeyboardRemove())
        await state.set_state("get_name")



@dp.message_handler(content_types=types.ContentTypes.TEXT, state="get_phone")
async def get_phone(message: types.Message, state: FSMContext):
    if isValid(message.text):
        user = await get_user(message.from_user.id)
        phone = message.text
        user.phone = phone
        user.save()
        await message.answer(text=f"Ismingizni kiriting 👇", reply_markup=ReplyKeyboardRemove())
        await state.set_state("get_name")
    else:
        markup = await phone_keyboard()
        await message.answer("Telefon raqamininfizni xalqaro formatda <b>998YYXXXXXXX</b> kabi kiriting. Yoki raqamni ulashing👇", reply_markup=markup)
        await state.set_state("get_phone")            
    
@dp.message_handler(content_types=types.ContentTypes.TEXT, state="get_name")
async def get_name(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    user.name = message.text
    user.save()
    # keyboard = forward_keyboard()
    keyboard = await main_keyboard()
    await message.answer(text=f"Siz konkursda muvaffaqqiyatli a’zo bo’ldingiz", reply_markup=keyboard )
    await state.set_state("main")


@dp.message_handler(content_types=types.ContentTypes.TEXT, state="main")
async def get_name(message: types.Message, state: FSMContext):
    if message.text == "Konkurs haqida":
        keyboard = await forward_keyboard()
        # keyboard = main_keyboard()
        await message.answer(text=f"Konkurs haqida ma'lumot", reply_markup=keyboard )
        await state.set_state("main")            
    elif message.text ==  "Xafta g'oliblari":
        winners = await get_week_winners()
        text = 'Ushbu xafta g\'oliblari: \n'
        i = 1
        for user in winners:
            text += "{i}){user.username}| {user.phone}| {user.name}"
        keyboard = await main_keyboard()
        await message.answer(text=text, reply_markup=keyboard)
        
        
