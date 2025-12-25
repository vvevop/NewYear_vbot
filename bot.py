from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram.filters import Command, CommandObject
from aiogram import Router
import logging, asyncio
    
from datetime import datetime
import pymorphy3
import hashlib


from bot_token import TOKEN
from config import my_id

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(

    )
)

dp = Dispatcher()
router = Router()

############################################################################################################################################

@dp.message(Command("---"))
async def get_password_async(message: types.Message):
    chat_id = message.chat.id
    username = message.chat.username

    if chat_id == my_id:
        123
    else:
        await message.answer("Недостаточно прав для доступа к боту 😇 \n\n" "<blockquote>Разработчик: @beaitch</blockquote>", parse_mode='HTML')
        await bot.send_message(chat_id = my_id, text = f"@{username} <code>{chat_id}</code> пытался получить доступ к боту\n" "#новый", parse_mode='HTML')

morph = pymorphy3.MorphAnalyzer()

######################################################################

def format_time(number, word_str):
    word = morph.parse(word_str)[0]
    agreed = word.make_agree_with_number(number).word
    return f"{number} {agreed}"

############################################################################################################################################

@dp.message(Command("start"))
async def start(message: types.Message):

    new_year = datetime(2026, 1, 1, 0, 0, 0)

    current_datetime = datetime.now()
    time_difference = new_year - current_datetime
    total_seconds_left = time_difference.total_seconds()

    days = total_seconds_left // 86400
    total_seconds_left %= 86400

    hours = total_seconds_left // 3600
    total_seconds_left %= 3600

    minutes = total_seconds_left // 60
    total_seconds_left %= 60

    seconds = total_seconds_left

    days = int(days)
    hours = int(hours)
    minutes = int(minutes)
    seconds = int(seconds)

    await message.answer(f"🎄 До нового года: \n" f"<blockquote><b>{format_time(days, 'день')} {format_time(hours, 'час')} {format_time(minutes, 'минута')} {format_time(seconds, 'секунда')}</b></blockquote>", parse_mode='HTML')

######################################################################

@router.inline_query()
async def query_handler(inline_query: InlineQuery):
    
    new_year = datetime(2026, 1, 1, 0, 0, 0)

    current_datetime = datetime.now()
    time_difference = new_year - current_datetime
    total_seconds_left = time_difference.total_seconds()

    days = total_seconds_left // 86400
    total_seconds_left %= 86400

    hours = total_seconds_left // 3600
    total_seconds_left %= 3600

    minutes = total_seconds_left // 60
    total_seconds_left %= 60

    seconds = total_seconds_left

    days = int(days)
    hours = int(hours)
    minutes = int(minutes)
    seconds = int(seconds)
    
    results = [
        InlineQueryResultArticle(
            id="1",
            title="🎄 Cколько осталось до нового года?", 
            description="Нажми сюда, чтобы узнать",
            input_message_content=InputTextMessageContent(
                message_text = f"🎄 До нового года: \n" f"<blockquote><b>{format_time(days, 'день')} {format_time(hours, 'час')} {format_time(minutes, 'минута')} {format_time(seconds, 'секунда')}</b></blockquote>", parse_mode='HTML'
            )
        )
    ]
    
    await inline_query.answer(results=results, cache_time=0)

############################################################################################################################################

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())