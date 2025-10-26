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
TOKEN = os.getenv("TOKEN") or "7597289189:AAEQ6feVesGHMvvOP5lPDHoDkMyVvc29umY"

# 🧠 Логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


# ---------- FSM ----------
class DeliveryCalc(StatesGroup):
    waiting_for_city = State()


# ---------- Клавиатуры ----------
def main_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Каталог (примеры работ)", callback_data="catalog")],
        [
            InlineKeyboardButton(text="💰 Стоимость", callback_data="price"),
            InlineKeyboardButton(text="🚚 Доставка", callback_data="delivery")
        ],
        [InlineKeyboardButton(text="🌐 Другие площадки", callback_data="socials")],
        [InlineKeyboardButton(text="💬 Связаться с менеджером", url="https://t.me/undercust_shop?start=bot")]
    ])


# ---------- /start ----------
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer_photo(
        photo="https://telegra.ph/file/79cc3eae3c8d9a2087e27.jpg",
        caption=(
            "👋 Привет! Это бот мастерской <b>undercust</b> — место, где кастом становится искусством.\n\n"
            "📢 Наш Telegram-канал: <a href='https://t.me/undercust_tgk'>@undercust_tgk</a>\n"
            "Там выходят свежие работы, новости и акции ⚙️"
        ),
        parse_mode="HTML"
    )
    await message.answer(
        "Здесь можно:\n"
        "• посмотреть <b>примеры работ</b>,\n"
        "• узнать <b>стоимость</b> и <b>доставку</b>,\n"
        "• оформить <b>индивидуальный заказ</b>.\n\n"
        "Выбирай, что интересует 👇",
        parse_mode="HTML",
        reply_markup=main_menu_kb()
    )


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
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=kb)


# ---------- Цурикавы ----------
@dp.callback_query(F.data == "tsurikawa")
async def show_tsurikawa(callback: types.CallbackQuery):
    photos = [
        "https://telegra.ph/file/ba35a99b47ef1a775a1b9.jpg",
        "https://telegra.ph/file/fafde7c2d4da6234148c4.jpg",
        "https://telegra.ph/file/b1c7a0d63157e4402a3d5.jpg",
        "https://telegra.ph/file/22ed76ef23b61e6b7eec3.jpg",
        "https://telegra.ph/file/dfe8d90e2a446f8c2f906.jpg"
    ]

    await callback.message.edit_text("🌀 <b>Примеры цурикав от undercust:</b>", parse_mode="HTML")

    for url in photos:
        try:
            await bot.send_photo(chat_id=callback.message.chat.id, photo=url)
            await asyncio.sleep(0.4)
        except Exception as e:
            logging.error(f"Ошибка при загрузке {url}: {e}")
            await bot.send_message(callback.message.chat.id, f"⚠️ Не удалось загрузить фото:\n{url}")

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад к каталогу", callback_data="catalog")]
    ])
    await bot.send_message(
        callback.message.chat.id,
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
        "❌ <b>Пока нет:</b> Porsche, Genesis, Dodge, Chrysler, Jeep, Tesla, Citroën, Ferrari, "
        "Lamborghini, Maserati, Mini, Land Rover, Jaguar, Bentley, Rolls-Royce, Chery, Haval, Omoda и др.\n\n"
        "💎 Со временем список будет пополняться."
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="catalog")]
    ])
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=kb)


# ---------- Стоимость ----------
@dp.callback_query(F.data == "price")
async def show_price(callback: types.CallbackQuery):
    text = (
        "💰 <b>Стоимость изделий</b>\n\n"
        "🔷 Эмблемы — от 1200 до 2000 ₽\n"
        "🔶 Цурикавы — 1800 ₽\n"
        "🔶 Брелки — 800 ₽\n"
        "🔶 Подвески — 1400 ₽\n"
        "🔶 Колпачки — 1400 ₽ (комплект)\n"
        "🔶 Шильдики / надписи — от 800 ₽\n\n"
        "Для точного расчёта — напишите менеджеру: @undercust_shop 💬"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_start")]
    ])
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=kb)


# ---------- Доставка ----------
@dp.callback_query(F.data == "delivery")
async def show_delivery(callback: types.CallbackQuery):
    text = (
        "🚚 <b>Доставка</b>\n\n"
        "📦 По России:\n"
        "• СДЭК — от 350 ₽ (быстро)\n"
        "• Яндекс.Доставка — дешевле, но чуть дольше\n"
        "• Ozon Посылка — акция 99 ₽ 🎯\n\n"
        "🌍 В страны СНГ — только СДЭК (от 700 ₽ / 10–25 дней)\n\n"
        "Отправка из Великого Новгорода 📦"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_start")]
    ])
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=kb)


# ---------- Назад ----------
@dp.callback_query(F.data == "back_to_start")
async def back_to_start(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Здесь можно:\n"
        "• посмотреть <b>примеры работ</b>,\n"
        "• узнать <b>стоимость</b> и <b>доставку</b>,\n"
        "• оформить <b>индивидуальный заказ</b>.\n\n"
        "Выбирай, что интересует 👇",
        parse_mode="HTML",
        reply_markup=main_menu_kb()
    )


# ---------- Запуск ----------
async def main():
    logging.info("Бот запускается...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())