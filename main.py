from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import (
    InlineQuery, InlineQueryResultArticle, InputTextMessageContent,
    ChosenInlineResult
)
from aiogram.filters import Command
from aiogram import Router
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

import logging, asyncio
from datetime import datetime
from zoneinfo import ZoneInfo
import pymorphy3
import aiohttp

from config import BOT_TOKEN, ADMIN_IDS, MY_ID, BOT_VERSION, HEARTBEAT_URL

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode='HTML'
    )
)

dp = Dispatcher()
router = Router()


@dp.message(Command("---"))
async def plug(message: types.Message):
    chat_id = message.chat.id
    username = message.chat.username

    if chat_id not in ADMIN_IDS:
        await message.answer("Недостаточно прав для доступа к боту 😇 \n\n" "<blockquote>Разработчик: @beaitch</blockquote>")
        await bot.send_message(chat_id = MY_ID, text = f"@{username} <code>{chat_id}</code> пытался получить доступ к боту\n" "#новый")
        return


morph = pymorphy3.MorphAnalyzer()

def format_time(number, word_str):
    
    word = morph.parse(word_str)[0]
    agreed = word.make_agree_with_number(number).word
    return f"{number} {agreed}"

def get_time_to_new_yearr():
    
    msk_tz = ZoneInfo("Europe/Moscow")
    current_datetime = datetime.now(msk_tz)
    new_year = datetime(current_datetime.year + 1, 1, 1, 0, 0, 0, tzinfo=msk_tz)
    
    time_difference = new_year - current_datetime
    total_s_left = time_difference.total_seconds()

    d = total_s_left // 86400; total_s_left %= 86400

    h = total_s_left // 3600; total_s_left %= 3600

    m = total_s_left // 60; total_s_left %= 60

    s = total_s_left

    d = int(d); h = int(h); m = int(m); s = int(s)

    return d, h, m, s

PREMIUM_TREE_EMOJI_ID = "4958563601775330153"

def get_update_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Обновить", callback_data="update_time")
    return kb.as_markup()

def get_new_year_text():
    d, h, m, s = get_time_to_new_yearr()

    text = (
        f'<tg-emoji emoji-id="{PREMIUM_TREE_EMOJI_ID}">🎄</tg-emoji> До нового года: \n'
        f"<blockquote><b>{format_time(d, 'день')} {format_time(h, 'час')} {format_time(m, 'минута')} {format_time(s, 'секунда')}</b></blockquote>"
    )
    return text

@dp.message(Command("start"))
async def start(message: types.Message):

    text = get_new_year_text()

    await message.answer(text, reply_markup=get_update_keyboard())

@dp.message(Command("version"))
async def version(message: types.Message):
    chat_id = message.chat.id
    username = message.chat.username

    if chat_id not in ADMIN_IDS:
        return
    
    await message.answer(f"🤖 Я работаю на версии <b>{BOT_VERSION}</b>")

@router.inline_query()
async def query_handler(inline_query: InlineQuery):

    kb = InlineKeyboardBuilder()
    kb.button(text="ㅤ", callback_data="ㅤ")

    results = [ 
        InlineQueryResultArticle(
            id="trea",
            title="🎄 Cколько осталось до нового года?", 
            description="Нажми сюда, чтобы узнать",
            input_message_content=InputTextMessageContent(
                message_text = "⁡",
                parse_mode="HTML"
            ),
            reply_markup=kb.as_markup()
        )
    ]
    
    await inline_query.answer(results=results, cache_time=0)

@router.chosen_inline_result()
async def inline_resulter(call: ChosenInlineResult, state: FSMContext):
    await state.clear()

    if not call.inline_message_id:
        return
    
    text = get_new_year_text()

    if call.result_id == "trea":
        try:
            await call.bot.edit_message_text(
                inline_message_id=call.inline_message_id,
                text=text,
                parse_mode="HTML",
                reply_markup=get_update_keyboard()
            )
        except Exception as e:
            print(f"Ошибка редактирования: {e}")


@dp.callback_query(F.data == "update_time")
async def update_time_callback_handler(callback_query: types.CallbackQuery):
    """
    Обрабатывает нажатие на кнопку "Обновить", обновляя время в сообщении.
    """
    new_text = get_new_year_text()
    
    try:
        if callback_query.inline_message_id:
            # Если это инлайн-сообщение
            await bot.edit_message_text(
                inline_message_id=callback_query.inline_message_id,
                text=new_text,
                reply_markup=get_update_keyboard()
            )
        elif callback_query.message:
            # Если это обычное сообщение
            await callback_query.message.edit_text(
                text=new_text,
                reply_markup=get_update_keyboard()
            )
        
        # Отправляем подтверждение, что колбэк обработан
        await callback_query.answer("Время обновлено!")

    except Exception as e:
        # В случае ошибки (например, сообщение слишком старое)
        logging.error(f"Ошибка при обновлении времени: {e}")
        await callback_query.answer("Не удалось обновить время.", show_alert=True)

async def heartbeat_task(url: str, interval: int = 60):
    """Асинхронная функция для пинга Better Stack"""
    print(f"[Heartbeat] Фоновая задача запущена. Интервал: {interval}с")
    
    # Создаем одну сессию для всех запросов (эффективнее)
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        logging.info(f"Heartbeat отправлен! Статус: {response.status}")
                    else:
                        logging.warning(f"Ошибка Heartbeat! Статус: {response.status}")
            except Exception as e:
                logging.error(f"Ошибка при пинге Heartbeat: {e}")
            
            # Важно: используем асинхронный сон, который не блокирует бота
            await asyncio.sleep(interval)
    
async def on_startup(bot: Bot):
    """Эта функция выполнится при запуске бота"""
    # Запускаем фоновую задачу
    asyncio.create_task(heartbeat_task(HEARTBEAT_URL, 60))

async def main():
    dp.include_router(router)

    # Регистрируем функцию, которая запустится при старте
    dp.startup.register(on_startup)

    await bot.delete_webhook(drop_pending_updates=True)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())