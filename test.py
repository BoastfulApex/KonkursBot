import hashlib
import logging
# from aiogram.dispatcher.handler import
from aiogram import types
from aiogram.dispatcher import FSMContext, handler
from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle, ChosenInlineResult

API_TOKEN = '5174048507:AAETwce-zQjx_wATisMOsDOrfeT08RToHjw'

# logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message):
    await message.answer("Salom")

@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery, state:FSMContext):
    text = inline_query.query or 'Kerakli shaharni kiriting'
    # print("AAAAAAAAAA", text)
    input_content = InputTextMessageContent(text)
    print("BBBBBBBBB", input_content)
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    item = InlineQueryResultArticle(
        id=result_id,
        title=f'{text!r}',
        input_message_content=input_content,
    )
    # don't forget to set cache_time=1 for testing (default is 300s or 5m)
    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)
    # await state.set_state("get_answer")
    
@dp.message_handler(state="*")
async def get_answer(message:types.Message, state:FSMContext):
    print("QQQQQQQQQQQQQQQQ")
    # print("AAAAAAAAA", answer.result["id"])

if __name__ == '__main__':
    executor.start_polling(dp)