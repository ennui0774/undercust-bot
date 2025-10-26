# -*- coding: utf-8 -*-
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InputMediaPhoto
)

# 🔐 Токен
TOKEN = os.getenv("TOKEN") or "7597289189:AAEQ6feVesGHMvvOP5lPDHoDkMyVvc29umY"

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
        if getattr(message, "photo", None):
            await message.delete()
            await message.answer(text, **kwargs)
        else:
            await message.edit_text(text, **kwargs)
    except Exception:
        await message.answer(text, **kwargs)


# ---------- Каталог ----------
@dp.callback_query(F.data == "catalog")
async def show_catalog(callback: types.CallbackQuery):
    text = (
        "📦 <b>Каталог (примеры работ)</b>\n\n"
        "Некоторые изделия мастерской — чтобы показать стиль и возможности.\n\n"
        "Ниже можно открыть каталог или посмотреть цурикавы прямо здесь 👇"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📂 Каталог VK", url="https://vk.com/market-227792089?display_albums=true&screen=group")],
        [InlineKeyboardButton(text="🌀 Цурикавы", callback_data="tsurikawa")],
        [InlineKeyboardButton(text="🚗 Моей марки нет в каталоге", callback_data="no_brand")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_start")]
    ])
    await safe_edit_text(callback.message, text, parse_mode="HTML", reply_markup=kb)


# ---------- Цурикавы ----------
@dp.callback_query(F.data == "tsurikawa")
async def show_tsurikawa(callback: types.CallbackQuery):
    # 🖼 сюда можешь вставить свои ссылки на фото (до 10 штук)
    photos = [
        InputMediaPhoto(media="https://i.postimg.cc/Gm5Q9M64/tsurikawa1.jpg", caption="🌀 Примеры цурикав от undercust"),
        InputMediaPhoto(media="https://i.postimg.cc/hPm3yVvG/tsurikawa2.jpg"),
        InputMediaPhoto(media="https://i.postimg.cc/ncTsg7ps/tsurikawa3.jpg"),
        InputMediaPhoto(media="https://i.postimg.cc/mD3gWMSs/tsurikawa4.jpg"),
        InputMediaPhoto(media="https://i.postimg.cc/RVqbtPQb/tsurikawa5.jpg"),
    ]

    await callback.message.answer_media_group(photos)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад к каталогу", callback_data="catalog")]
    ])
    await callback.message.answer(
        "💎 <b>Цурикавы</b> — стильный акриловый аксессуар для автомобиля.\n\n"
        "• Цена: <b>1800 ₽</b>\n"
        "• Материалы: зеркальный и матовый акрил\n"
        "• Толщина: 6 мм\n"
        "• Изготовление до 10 рабочих дней\n\n"
        "👇 Вернуться в каталог можно ниже:",
        parse_mode="HTML",
        reply_markup=kb
    )


# ---------- Моей марки нет ----------
@dp.callback_query(F.data == "no_brand")
async def no_brand(callback: types.CallbackQuery):
    text = (
        "⚙️ <b>В разработке:</b> Renault, Daihatsu, Peugeot, Alfa Romeo, Cadillac.\n\n"
        "❌ <b>Пока нет:</b> Porsche, Genesis, Dodge, Chrysler, Jeep, Tesla, Citroën, Lancia, Ferrari, "
        "Lamborghini, Maserati, Mini, Land Rover, Range Rover, Jaguar, Aston Martin, Bentley, Rolls-Royce, "
        "Chery, Geely, Haval, Exeed, Great Wall, JAC, Omoda, Changan, Москвич, УАЗ, Volvo, Saab.\n\n"
        "💎 Со временем список будет пополняться."
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Назад", callback_data="catalog")]])
    await safe_edit_text(callback.message, text, parse_mode="HTML", reply_markup=kb)


# ---------- Стоимость ----------
@dp.callback_query(F.data == "price")
async def show_price(callback: types.CallbackQuery):
    text = (
        "💰 <b>Стоимость изделий</b>\n\n"
        "🔷 <b>Эмблемы</b>\n"
        "• Маленькие — <b>1200–1600 ₽</b>\n"
        "• Стандартные — <b>1800 ₽</b>\n"
        "• Большие / сложные — <b>от 2000 ₽</b>\n\n"
        "🔶 <b>Другие изделия</b>\n"
        "• Цурикавы — 1800 ₽\n"
        "• Брелки — 800 ₽\n"
        "• Подвески — 1400 ₽\n"
        "• Колпачки — 1400 ₽ (комплект)\n"
        "• Шильдики / надписи — от 800 ₽ (зависит от размеров и сложности)\n\n"
        "Для точного расчёта по вашей модели — напишите менеджеру: @undercust_shop 💬"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_start")]])
    await safe_edit_text(callback.message, text, parse_mode="HTML", reply_markup=kb)


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
        "Отправка из Великого Новгорода.\n"
        "👇 Можно рассчитать стоимость:"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Рассчитать доставку", callback_data="calc_delivery")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_start")]
    ])
    await safe_edit_text(callback.message, text, parse_mode="HTML", reply_markup=kb)


# ---------- Рассчитать доставку ----------
@dp.callback_query(F.data == "calc_delivery")
async def ask_city(callback: types.CallbackQuery, state: FSMContext):
    text = "Введите ваш город или страну.\nОтправка осуществляется из Великого Новгорода:"
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Отмена", callback_data="back_to_start")]])
    await safe_edit_text(callback.message, text, reply_markup=kb)
    await state.set_state(DeliveryCalc.waiting_for_city)


# ---------- Приём города ----------
@dp.message(DeliveryCalc.waiting_for_city)
async def calc_result(message: types.Message, state: FSMContext):
    city = message.text.strip().lower()
    near = ["москва", "санкт", "питер", "псков", "тверь", "новгород"]
    mid = ["казань", "нижний", "самара", "екатеринбург", "челябинск", "воронеж", "ростов"]
    far = ["владивосток", "хабаровск", "камчат", "петропавловск", "иркутск", "омск", "красноярск", "новосибирск"]
    cis = [
        "казахстан", "астана", "алматы", "караганда", "беларусь", "минск", "гомель",
        "армения", "ереван", "киргиз", "бишкек", "грузия", "тбилиси", "узбекистан", "ташкент",
        "таджикистан", "душанбе", "азербайджан", "баку"
    ]

    if any(w in city for w in cis):
        region = "Страны СНГ"
        sdek = "СДЭК — от 700 ₽ / 10–25 дней"
        yandex = "Яндекс.Доставка — недоступна"
        ozon = "Ozon Посылка — недоступна"
    elif any(w in city for w in near):
        region = "Ближний регион"
        sdek = "СДЭК 350–400 ₽ / 1–3 дня"
        yandex = "Яндекс 300–400 ₽ / 2–4 дня"
        ozon = "Ozon 99–300 ₽ / 3–5 дней"
    elif any(w in city for w in mid):
        region = "Среднее расстояние"
        sdek = "СДЭК 450–650 ₽ / 3–7 дней"
        yandex = "Яндекс 400–600 ₽ / 4–8 дней"
        ozon = "Ozon 200–400 ₽ / 5–9 дней"
    elif any(w in city for w in far):
        region = "Дальний регион"
        sdek = "СДЭК 700–950 ₽ / 15–30 дней"
        yandex = "Яндекс 600–850 ₽ / 20–35 дней"
        ozon = "Ozon 400–700 ₽ / 25–40 дней"
    else:
        region = "Регион не определён точно"
        sdek = "СДЭК от 400 ₽ / 3–10 дней"
        yandex = "Яндекс от 350 ₽ / 4–10 дней"
        ozon = "Ozon от 150 ₽ / 5–12 дней"

    await message.answer(
        f"📦 <b>Расчёт для:</b> {message.text.strip().title()}\n\n"
        f"Отправка — из Великого Новгорода\n\n"
        f"<b>{region}</b>\n\n{sdek}\n{yandex}\n{ozon}\n\n"
        "Цены и сроки ориентировочные и могут отличаться.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="⬅️ В меню", callback_data="back_to_start")]]
        )
    )
    await state.clear()


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
    asyncio.run(main())