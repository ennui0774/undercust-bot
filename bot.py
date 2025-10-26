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
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


# ---------- FSM ----------
class DeliveryCalc(StatesGroup):
    waiting_for_city = State()


# ---------- Главное меню ----------
def main_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Каталог (примеры работ)", callback_data="catalog")],
        [
            InlineKeyboardButton(text="💰 Стоимость", callback_data="price"),
            InlineKeyboardButton(text="🚚 Доставка", callback_data="delivery")
        ],
        [InlineKeyboardButton(text="❓ Часто задаваемые вопросы", callback_data="faq_menu")],
        [InlineKeyboardButton(text="💬 Связаться с менеджером", url="https://t.me/undercust_shop")]
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
            "👋 Привет!\n"
            "Это бот мастерской <b>undercust</b> — место, где кастом становится искусством.\n\n"
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
async def safe_edit(message: types.Message, text: str, **kwargs):
    try:
        if message.photo:
            await message.edit_caption(caption=text, **kwargs)
        else:
            await message.edit_text(text=text, **kwargs)
    except Exception:
        await message.answer(text, **kwargs)


# ---------- Каталог ----------
@dp.callback_query(F.data == "catalog")
async def show_catalog(callback: types.CallbackQuery):
    text = (
        "📦 <b>Каталог (примеры работ)</b>\n\n"
        "Выберите категорию изделий или откройте наш альбом VK 👇"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📂 Открыть каталог VK",
            url="https://vk.com/market-227792089?display_albums=true&screen=group"
        )],
        [InlineKeyboardButton(text="💀 Цурикавы", callback_data="catalog_tsurikawa")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_start")]
    ])

    await safe_edit(callback.message, text, parse_mode="HTML", reply_markup=kb)


# ---------- Цурикавы ----------
@dp.callback_query(F.data == "catalog_tsurikawa")
async def show_tsurikawas(callback: types.CallbackQuery):
    text = (
        "💀 <b>Цурикавы</b>\n\n"
        "Каждая выполнена из акрила, с возможностью выбора цветов.\n"
        "⚠️ Предназначены только для использования в салоне — не из ударопрочного материала."
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👹 Демон Они — 1800 ₽", callback_data="tsurikawa_oni")],
        [InlineKeyboardButton(text="💜 Сердце с рогами (гравировка) — 1600 ₽", callback_data="tsurikawa_heart")],
        [InlineKeyboardButton(text="🦋 Бабочка — 1800 ₽", callback_data="tsurikawa_butterfly")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="catalog")]
    ])

    await safe_edit(callback.message, text, parse_mode="HTML", reply_markup=kb)


# ---------- Они ----------
@dp.callback_query(F.data == "tsurikawa_oni")
async def show_tsurikawa_oni(callback: types.CallbackQuery):
    photos = [
        "https://disk.yandex.ru/i/W5uiIGsrRCuuVw",
        "https://disk.yandex.ru/i/QbQNT-ATOz-c3A",
        "https://disk.yandex.ru/i/ApAsbNGD5crP5g",
        "https://disk.yandex.ru/i/6QxDkQCR4B0ETw"
    ]
    for link in photos:
        await bot.send_photo(callback.message.chat.id, photo=link)

    text = (
        "👹 <b>Цурикава «Демон Они»</b>\n\n"
        "Цена: 1800 ₽\n"
        "Можно выбрать цвета акрила.\n"
        "⚠️ Только для использования в салоне."
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад к цурикавам", callback_data="catalog_tsurikawa")],
        [InlineKeyboardButton(text="💬 Заказать", url="https://t.me/undercust_shop")]
    ])

    await callback.message.answer(text, parse_mode="HTML", reply_markup=kb)


# ---------- Сердце ----------
@dp.callback_query(F.data == "tsurikawa_heart")
async def show_tsurikawa_heart(callback: types.CallbackQuery):
    photos = [
        "https://disk.yandex.ru/i/8QT9IeO9fdVEsA",
        "https://disk.yandex.ru/i/luJokqiCeM20aw"
    ]
    for link in photos:
        await bot.send_photo(callback.message.chat.id, photo=link)

    text = (
        "💜 <b>Цурикава «Сердце с рогами»</b>\n\n"
        "Цена: 1600 ₽\n"
        "С лазерной гравировкой и возможностью смены цветов.\n"
        "⚠️ Только для использования в салоне."
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад к цурикавам", callback_data="catalog_tsurikawa")],
        [InlineKeyboardButton(text="💬 Заказать", url="https://t.me/undercust_shop")]
    ])

    await callback.message.answer(text, parse_mode="HTML", reply_markup=kb)


# ---------- Бабочка ----------
@dp.callback_query(F.data == "tsurikawa_butterfly")
async def show_tsurikawa_butterfly(callback: types.CallbackQuery):
    photos = [
        "https://disk.yandex.ru/i/SnWR-phg5zUJww",
        "https://disk.yandex.ru/i/lwE19C7SL4OrIg",
        "https://disk.yandex.ru/i/R0PHB8mjhtNKSQ"
    ]
    for link in photos:
        await bot.send_photo(callback.message.chat.id, photo=link)

    text = (
        "🦋 <b>Цурикава «Бабочка»</b>\n\n"
        "Цена: 1800 ₽\n"
        "Можно выбрать цвета акрила.\n"
        "⚠️ Только для использования в салоне."
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад к цурикавам", callback_data="catalog_tsurikawa")],
        [InlineKeyboardButton(text="💬 Заказать", url="https://t.me/undercust_shop")]
    ])

    await callback.message.answer(text, parse_mode="HTML", reply_markup=kb)


# ---------- Стоимость ----------
@dp.callback_query(F.data == "price")
async def show_price(callback: types.CallbackQuery):
    text = (
        "💰 <b>Стоимость изделий</b>\n\n"
        "• Эмблемы — 1800 ₽ (возможны исключения)\n"
        "• Цурикавы — от 1600 ₽ до 1800 ₽\n"
        "• Брелки — 800 ₽\n"
        "• Подвески — 1400 ₽\n"
        "• Колпачки — 1400 ₽\n"
        "• Шильдики / надписи — от 800 ₽ (зависит от размеров)\n\n"
        "Для уточнения — @undercust_shop 💬"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_start")]
    ])
    await safe_edit(callback.message, text, parse_mode="HTML", reply_markup=kb)


# ---------- Доставка ----------
@dp.callback_query(F.data == "delivery")
async def show_delivery(callback: types.CallbackQuery):
    text = (
        "🚚 <b>Доставка</b>\n\n"
        "<b>📦 По России:</b>\n"
        "• СДЭК — от 350 ₽ (быстро)\n"
        "• Яндекс.Доставка — дешевле, но чуть дольше\n"
        "• Ozon Посылка — акция 99 ₽ 🎯\n\n"
        "<b>🌍 В страны СНГ:</b> только СДЭК — от 700 ₽ / 10–25 дней\n\n"
        "Отправка из Великого Новгорода."
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_start")]
    ])
    await safe_edit(callback.message, text, parse_mode="HTML", reply_markup=kb)


# ---------- FAQ ----------
@dp.callback_query(F.data == "faq_menu")
async def faq_menu(callback: types.CallbackQuery):
    text = "❓ <b>Часто задаваемые вопросы</b>\n\n👇 Выберите интересующий вопрос:"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛠 Как оформить заказ", callback_data="faq_order")],
        [InlineKeyboardButton(text="📎 Крепление эмблемы", callback_data="faq_mount")],
        [InlineKeyboardButton(text="🎨 Индивидуальный дизайн", callback_data="faq_design")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_start")]
    ])
    await safe_edit(callback.message, text, parse_mode="HTML", reply_markup=kb)


faq_answers = {
    "faq_order": (
        "🛠 <b>Как оформить заказ?</b>\n\n"
        "Можно выбрать готовый дизайн или заказать индивидуальный.\n"
        "После согласования макета уточняем детали, беру предоплату и запускаю в работу."
    ),
    "faq_mount": (
        "📎 <b>Как крепится эмблема?</b>\n\n"
        "На заднюю поверхность наносится прочный 3М-скотч.\n"
        "Перед установкой очистите и обезжирьте поверхность."
    ),
    "faq_design": (
        "🎨 <b>Можно ли сделать индивидуальный дизайн?</b>\n\n"
        "Да! Напишите менеджеру 👉 <a href='https://t.me/undercust_shop'>@undercust_shop</a>"
    )
}


@dp.callback_query(F.data.in_(faq_answers.keys()))
async def show_faq_answer(callback: types.CallbackQuery):
    answer = faq_answers[callback.data]
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад к вопросам", callback_data="faq_menu")],
        [InlineKeyboardButton(text="⬅️ В меню", callback_data="back_to_start")]
    ])
    await safe_edit(callback.message, answer, parse_mode="HTML", reply_markup=kb)


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
    try:
        await bot.delete_webhook(drop_pending_updates=True)
    except Exception as e:
        logging.warning(f"Не удалось удалить webhook: {e}")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен вручную.")




