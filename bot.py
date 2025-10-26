# -*- coding: utf-8 -*-
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

# 🔐 Токен
TOKEN = os.getenv("TOKEN") or "7597289189:AAEQ6feVesGHMvvOP5lPDHoDkMyVvc29umY"

# 🧠 Логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

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

    # Отправляем фото только один раз
    await message.answer_photo(
        photo="https://i.postimg.cc/sgCn32q0/photo-2025-10-23-21-02-28.jpg",
        caption=(
            "👋 Привет! Это бот мастерской <b>undercust</b> — место, где кастом становится искусством.\n\n"
            "📢 Наш Telegram-канал: <a href='https://t.me/undercust_tgk'>@undercust_tgk</a>\n"
            "Там выходят свежие работы, новости и акции ⚙️"
        ),
        parse_mode="HTML"
    )

    # Главное меню отдельно
    await message.answer(
        "Здесь можно:\n"
        "• посмотреть <b>примеры работ</b>,\n"
        "• узнать <b>стоимость</b> и <b>доставку</b>,\n"
        "• задать вопросы или оформить <b>индивидуальный заказ</b>.\n\n"
        "Выбирай, что интересует 👇",
        parse_mode="HTML",
        reply_markup=main_menu_kb()
    )


# ---------- Безопасное редактирование ----------
async def safe_edit_text(message: types.Message, text: str, **kwargs):
    try:
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
    photos = [
        InputMediaPhoto(media="https://i.postimg.cc/Gm5Q9M64/tsurikawa1.jpg", caption="🌀 Примеры цурикав от undercust"),
        InputMediaPhoto(media="https://i.postimg.cc/hPm3yVvG/tsurikawa2.jpg"),
        InputMediaPhoto(media="https://i.postimg.cc/ncTsg7ps/tsurikawa3.jpg"),
        InputMediaPhoto(media="https://i.postimg.cc/mD3gWMSs/tsurikawa4.jpg"),
        InputMediaPhoto(media="https://i.postimg.cc/RVqbtPQb/tsurikawa5.jpg"),
    ]

    try:
        await bot.send_media_group(chat_id=callback.message.chat.id, media=photos)
    except Exception as e:
        await callback.message.answer("⚠️ Не удалось загрузить альбом. Попробуйте ещё раз чуть позже.")
        logging.error(f"Ошибка при отправке цурикав: {e}")
        return

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
        "❌ <b>Пока нет:</b> Porsche, Genesis, Dodge, Chrysler, Jeep, Tesla, Citroën, Ferrari, "
        "Lamborghini, Maserati, Mini, Land Rover, Jaguar, Bentley, Rolls-Royce, Chery, Haval, Omoda и др.\n\n"
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
        "Для точного расчёта — напишите менеджеру: @undercust_shop 💬"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_start")]])
    await safe_edit_text(callback.message, text, parse_mode="HTML", reply_markup=kb)


# ---------- Назад ----------
@dp.callback_query(F.data == "back_to_start")
async def back_to_start(callback: types.CallbackQuery):
    await safe_edit_text(
        callback.message,
        "Здесь можно:\n"
        "• посмотреть <b>примеры работ</b>,\n"
        "• узнать <b>стоимость</b> и <b>доставку</b>,\n"
        "• задать вопросы или оформить <b>индивидуальный заказ</b>.\n\n"
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