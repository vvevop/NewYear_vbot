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

from config import BOT_TOKEN, ADMIN_IDS, MY_ID, BOT_VERSION

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=BOT_TOKEN,
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

    if chat_id in ADMIN_IDS:
        123
    else:
        await message.answer("Недостаточно прав для доступа к боту 😇 \n\n" "<blockquote>Разработчик: @beaitch</blockquote>", parse_mode='HTML')
        await bot.send_message(chat_id = MY_ID, text = f"@{username} <code>{chat_id}</code> пытался получить доступ к боту\n" "#новый", parse_mode='HTML')

morph = pymorphy3.MorphAnalyzer()

######################################################################

def format_time(number, word_str):
    word = morph.parse(word_str)[0]
    agreed = word.make_agree_with_number(number).word
    return f"{number} {agreed}"

def get_time_to_new_yearr():
    
    current_datetime = datetime.now()
    
    new_year = datetime(current_datetime.year + 1, 1, 1, 0, 0, 0)

    current_datetime = datetime.now()
    time_difference = new_year - current_datetime
    total_s_left = time_difference.total_seconds()

    d = total_s_left // 86400
    total_s_left %= 86400

    h = total_s_left // 3600
    total_s_left %= 3600

    m = total_s_left // 60
    total_s_left %= 60

    s = total_s_left

    d = int(d)
    h = int(h)
    m = int(m)
    s = int(s)

    return d, h, m, s

############################################################################################################################################

@dp.message(Command("start"))
async def start(message: types.Message):

    d, h, m, s = get_time_to_new_yearr()

    await message.answer(f"🎄 До нового года: \n" f"<blockquote><b>{format_time(d, 'день')} {format_time(h, 'час')} {format_time(m, 'минута')} {format_time(s, 'секунда')}</b></blockquote>", parse_mode='HTML')

######################################################################

@router.inline_query()
async def query_handler(inline_query: InlineQuery):
    
    d, h, m, s = get_time_to_new_yearr()
    
    results = [
        InlineQueryResultArticle(
            id="1",
            title="🎄 Cколько осталось до нового года?", 
            description="Нажми сюда, чтобы узнать",
            input_message_content=InputTextMessageContent(
                message_text = f"🎄 До нового года: \n" f"<blockquote><b>{format_time(d, 'день')} {format_time(h, 'час')} {format_time(m, 'минута')} {format_time(s, 'секунда')}</b></blockquote>", parse_mode='HTML'
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