
import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

API_TOKEN = 'YOUR_BOT_TOKEN_HERE'  # 🔁 Замінити на свій токен

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Кнопки
register_url = "https://u3.shortink.io/register?utm_campaign=819083&utm_source=affiliate&utm_medium=sr&a=Df4ek3JlsrzSid&ac=tgchanel&code=50START"

# Кнопки мов
lang_kb = InlineKeyboardMarkup().add(
    InlineKeyboardButton("🇺🇦 Українська", callback_data="lang_uk"),
    InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
)

# Стратегія кнопка
strategy_btn_uk = InlineKeyboardMarkup().add(
    InlineKeyboardButton("📘 Отримати стратегію", callback_data="strategy_uk")
)
strategy_btn_en = InlineKeyboardMarkup().add(
    InlineKeyboardButton("📘 Get strategy", callback_data="strategy_en")
)

register_btn = InlineKeyboardMarkup().add(
    InlineKeyboardButton("🔗 Зареєструватися", url=register_url)
)
register_btn_en = InlineKeyboardMarkup().add(
    InlineKeyboardButton("🔗 Register", url=register_url)
)

# Стани користувачів
user_lang = {}

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Choose your language / Обери мову:", reply_markup=lang_kb)

@dp.callback_query_handler(lambda c: c.data.startswith('lang_'))
async def set_language(callback_query: types.CallbackQuery):
    lang = callback_query.data.split('_')[1]
    user_lang[callback_query.from_user.id] = lang
    await bot.answer_callback_query(callback_query.id)
    if lang == 'uk':
        await bot.send_message(callback_query.from_user.id,
            "Привіт! Це PocketSignal1D 🤖

Я надсилатиму тобі сигнали для торгівлі на Pocket Option.

Почни із реєстрації:", reply_markup=register_btn)
        await bot.send_message(callback_query.from_user.id,
            "📘 Хочеш дізнатися просту стратегію?", reply_markup=strategy_btn_uk)
    else:
        await bot.send_message(callback_query.from_user.id,
            "Hi! This is PocketSignal1D 🤖

I will send you trading signals for Pocket Option.

Start with registration:", reply_markup=register_btn_en)
        await bot.send_message(callback_query.from_user.id,
            "📘 Want a simple strategy?", reply_markup=strategy_btn_en)

@dp.callback_query_handler(lambda c: c.data == 'strategy_uk')
async def strategy_info_uk(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
        "Стратегія "3 із 5":

1. Обери EUR/USD.
2. Увімкни індикатор RSI.
3. Якщо RSI < 30 — став ВГОРУ.
4. Якщо RSI > 70 — став ВНИЗ.
5. Зроби 5 угод по $1.
3+ угоди в плюс — ти в заробітку 💸")

@dp.callback_query_handler(lambda c: c.data == 'strategy_en')
async def strategy_info_en(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
        ""3 of 5" Strategy:

1. Choose EUR/USD.
2. Enable RSI indicator.
3. If RSI < 30 — trade UP.
4. If RSI > 70 — trade DOWN.
5. Make 5 trades of $1.
If 3+ are in profit — you win 💸")

# Фейкові сигнали (рандом)
assets = ["EUR/USD", "GBP/USD", "BTC/USD", "ETH/USD"]
directions = ["ВГОРУ", "ВНИЗ"]
directions_en = ["UP", "DOWN"]

async def send_fake_signals():
    while True:
        await asyncio.sleep(600)  # кожні 10 хвилин
        for chat_id in registered_users:
            try:
                lang = user_lang.get(chat_id, 'uk')
                if lang == 'uk':
                    signal = f"💡 Сигнал:
Актив: {random.choice(assets)}
Напрям: {random.choice(directions)}
Час: {random.randint(1,3)} хвилини
Ставка: $1"
                else:
                    signal = f"💡 Signal:
Asset: {random.choice(assets)}
Direction: {random.choice(directions_en)}
Time: {random.randint(1,3)} minutes
Amount: $1"
                await bot.send_message(chat_id, signal)
            except:
                pass

# Зберігання ID користувачів
registered_users = set()

@dp.message_handler()
async def handle_all(message: types.Message):
    registered_users.add(message.chat.id)

# Запуск бота
async def on_startup(_):
    asyncio.create_task(send_fake_signals())

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
