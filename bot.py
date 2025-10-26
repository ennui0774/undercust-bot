# -*- coding: utf-8 -*-
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🔐 Токен
TOKEN = os.getenv("TOKEN") or "7597289189:AAHwJUyLM99LIUm6hwFH52dxiO1GtnjPot4"

# 🧠 Логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# 🚀 Инициализация бота
bot = Bot(token=TOKEN)

# 👇 Эта строка очищает старые сессии Telegram (фикс ошибки Conflict)
asyncio.run(bot.delete_webhook(drop_pending_updates=True))

dp = Dispatcher(storage=MemoryStorage())


# ---------- FSM ----------
class DeliveryCalc(StatesGroup):
    waiting_for_city = State()


# ---------- Главная клавиатура ----------
def main_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Каталог (примеры работ)", callback_data="catalog")],
        [
            InlineKeyboardButton(text="💰 Стоимость", callback_data="price"),
            InlineKeyboardButton(text="🚚 Доставка", callback_data="delivery")
        ],
        [InlineKeyboardButton(text="❓ Часто задаваемые вопросы", callback_data="faq_menu")],
        [InlineKeyboardButton(text="🌐 Другие площадки", callback_data="socials")],
        [InlineKeyboardButton(text="💬 Связаться с менеджером", url="https://t.me/undercust_shop?start=bot")]
    ])


# ---------- /start ----------
@dp.message(Command("start"))
async def start(message: types.Message):
    try:
        await message.delete()
    except Exception:
        pass

    await message.answer_photo(
        photo="https://i.postimg.cc/sgCn32q0/photo-2025-10-23-21-02-28.jpg",
        caption=(
            "👋 Привет! Это бот мастерской <b>undercust</b> — место, где кастом становится искусством.\n\n"
            "📢 Наш Telegram-канал: <a href='https://t.me/undercust_tgk'>@undercust_tgk</a>\n"
            "Там выходят свежие работы, новости и акции мастерской ⚙️"
        ),
        parse_mode="HTML"
    )

    await message.answer(
        text=(
            "Здесь можно:\n"
            "• посмотреть <b>примеры работ</b>,\n"
            "• узнать <b>стоимость</b> и <b>доставку</b>,\n"
            "• задать вопросы или оформить <b>индивидуальный заказ</b>.\n\n"
            "Выбирай, что интересует 👇"
        ),
        parse_mode="HTML",
        reply_markup=main_menu_kb()
    )


# ---------- Безопасное редактирование ----------
async def safe_edit_text(message: types.Message, text: str, **kwargs):
    try:
        if message.photo:
            await message.delete()
            await message.answer(text, **kwargs)
        else:
            await message.edit_text(text, **kwargs)
    except Exception:
        await message.answer(text, **kwargs)


# ---------- Каталог ----------
@dp.callback_query(F.data == "catalog")
async def show_catalog(callback: types.CallbackQuery):
    text = "📦 <b>Каталог изделий</b>\n\nВыберите категорию 👇"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Цурикавы", callback_data="catalog_tsurikawa")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_start")]
    ])
    await safe_edit_text(callback.message, text, parse_mode="HTML", reply_markup=kb)


# ---------- Каталог / Цурикавы ----------
@dp.callback_query(F.data == "catalog_tsurikawa")
async def tsurikawa_menu(callback: types.CallbackQuery):
    text = "🔗 <b>Цурикавы</b>\n\nВыберите модель 👇"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👹 Демон Они", callback_data="tsurikawa_oni")],
        [InlineKeyboardButton(text="💜 Демонское сердце", callback_data="tsurikawa_heart")],
        [InlineKeyboardButton(text="🦋 Бабочка", callback_data="tsurikawa_butterfly")],
        [InlineKeyboardButton(text="⬅️ Назад к каталогу", callback_data="catalog")]
    ])
    await safe_edit_text(callback.message, text, parse_mode="HTML", reply_markup=kb)


# ---------- Цурикава: Демон Они ----------
@dp.callback_query(F.data == "tsurikawa_oni")
async def tsurikawa_oni(callback: types.CallbackQuery):
    photos = [
        "https://disk.yandex.ru/i/W5uiIGsrRCuuVw",
        "https://disk.yandex.ru/i/QbQNT-ATOz-c3A",
        "https://disk.yandex.ru/i/ApAsbNGD5crP5g"
    ]
    text = (
        "👹 <b>Цурикава “Демон Они”</b>\n\n"
        "Символ силы и защиты. Классическая модель из зеркального акрила — сочетание аккуратности и агрессии.\n\n"
        "💰 Стоимость — 1800 ₽\n"
        "🎨 Цвета можно менять под ваш вкус.\n"
        "❗ Внимание: изделие выполнено из декоративного акрила и не является ударопрочным. "
        "Предназначено только для использования в салоне автомобиля."
    )
    for p in photos:
        await callback.message.answer_photo(photo=p)
    await callback.message.answer(text, parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад к цурикавам", callback_data="catalog_tsurikawa")],
            [InlineKeyboardButton(text="⬅️ В меню", callback_data="back_to_start")]
        ]))


# ---------- Цурикава: Демонское сердце ----------
@dp.callback_query(F.data == "tsurikawa_heart")
async def tsurikawa_heart(callback: types.CallbackQuery):
    photos = [
        "https://disk.yandex.ru/i/8QT9IeO9fdVEsA",
        "https://disk.yandex.ru/i/luJokqiCeM20aw"
    ]
    text = (
        "💜 <b>Цурикава “Демонское сердце”</b>\n\n"
        "Сердце с рожками и подтеками — символ страсти и хаоса. "
        "Имеет <b>лазерную гравировку</b>, подчёркивающую глубину и детали.\n\n"
        "💰 Стоимость — 1600 ₽\n"
        "🎨 Цвета можно менять под ваш вкус.\n"
        "❗ Внимание: изделие выполнено из декоративного акрила и не является ударопрочным. "
        "Предназначено только для использования в салоне автомобиля."
    )
    for p in photos:
        await callback.message.answer_photo(photo=p)
    await callback.message.answer(text, parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад к цурикавам", callback_data="catalog_tsurikawa")],
            [InlineKeyboardButton(text="⬅️ В меню", callback_data="back_to_start")]
        ]))


# ---------- Цурикава: Бабочка ----------
@dp.callback_query(F.data == "tsurikawa_butterfly")
async def tsurikawa_butterfly(callback: types.CallbackQuery):
    photos = [
        "https://disk.yandex.ru/i/SnWR-phg5zUJww",
        "https://disk.yandex.ru/i/lwE19C7SL4OrIg"
    ]
    text = (
        "🦋 <b>Цурикава “Бабочка”</b>\n\n"
        "Символ лёгкости и внутреннего равновесия. Минималистичная форма из зеркального акрила.\n\n"
        "💰 Стоимость — 1800 ₽\n"
        "🎨 Цвета можно менять под ваш вкус.\n"
        "❗ Внимание: изделие выполнено из декоративного акрила и не является ударопрочным. "
        "Предназначено только для использования в салоне автомобиля."
    )
    for p in photos:
        await callback.message.answer_photo(photo=p)
    await callback.message.answer(text, parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад к цурикавам", callback_data="catalog_tsurikawa")],
            [InlineKeyboardButton(text="⬅️ В меню", callback_data="back_to_start")]
        ]))


# ---------- Назад ----------
@dp.callback_query(F.data == "back_to_start")
async def back_to_start(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
    except Exception:
        pass
    await start(callback.message)


# ---------- Запуск ----------
async def main():
    logging.info("Бот запускается...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    import nest_asyncio
    import asyncio

    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())




