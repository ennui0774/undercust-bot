# -*- coding: utf-8 -*-
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🔐 Токен
TOKEN = os.getenv("TOKEN") or "7597289189:AAEQ6feVesGHMvvOP5lPDHoDkMyVvc29umY"

# 🧠 Логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


# ---------- Клавиатура ----------
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Каталог (примеры работ)", callback_data="catalog")],
        [
            InlineKeyboardButton(text="💰 Стоимость", callback_data="price"),
            InlineKeyboardButton(text="🚚 Доставка", callback_data="delivery"),
        ],
        [InlineKeyboardButton(text="🌐 Другие площадки", callback_data="socials")],
        [InlineKeyboardButton(text="💬 Связаться с менеджером", url="https://t.me/undercust_shop")]
    ])


# ---------- /start ----------
@dp.message(Command("start"))
async def start_cmd(msg: types.Message):
    await msg.answer_photo(
        "https://i.imgur.com/2vD5Sxg.jpeg",
        caption=(
            "👋 Привет! Это бот мастерской <b>undercust</b> — место, где кастом становится искусством.\n\n"
            "📢 Наш Telegram-канал: <a href='https://t.me/undercust_tgk'>@undercust_tgk</a>\n"
            "Там выходят свежие работы, новости и акции ⚙️"
        ),
        parse_mode="HTML",
    )

    await msg.answer(
        "Здесь можно:\n"
        "• посмотреть <b>примеры работ</b>,\n"
        "• узнать <b>стоимость</b> и <b>доставку</b>,\n"
        "• оформить <b>индивидуальный заказ</b>.\n\n"
        "Выбирай, что интересует 👇",
        parse_mode="HTML",
        reply_markup=main_menu(),
    )


# ---------- Каталог ----------
@dp.callback_query(F.data == "catalog")
async def show_catalog(cb: types.CallbackQuery):
    text = (
        "📦 <b>Каталог (примеры работ)</b>\n\n"
        "Некоторые изделия мастерской — чтобы показать стиль и возможности.\n\n"
        "Ниже можно открыть каталог или посмотреть цурикавы прямо здесь 👇"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📂 Каталог VK", url="https://vk.com/market-227792089?display_albums=true")],
        [InlineKeyboardButton(text="🌀 Цурикавы", callback_data="tsurikawa")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_start")]
    ])
    await cb.message.edit_text(text, parse_mode="HTML", reply_markup=kb)


# ---------- Цурикавы ----------
@dp.callback_query(F.data == "tsurikawa")
async def show_tsurikawa(cb: types.CallbackQuery):
    # стабильные картинки с imgur
    photos = [
        "https://i.imgur.com/sYqv6Cj.jpg",
        "https://i.imgur.com/Y4XZNyC.jpg",
        "https://i.imgur.com/3lG0ehB.jpg",
        "https://i.imgur.com/Gn5CVkU.jpg",
    ]

    await cb.message.edit_text("🌀 <b>Примеры цурикав от undercust:</b>", parse_mode="HTML")
    for url in photos:
        try:
            await bot.send_photo(cb.message.chat.id, url)
            await asyncio.sleep(0.4)
        except Exception as e:
            logging.error(f"Ошибка при фото {url}: {e}")
            await bot.send_message(cb.message.chat.id, f"⚠️ Не удалось загрузить фото: {url}")

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад в каталог", callback_data="catalog")]
    ])
    await bot.send_message(
        cb.message.chat.id,
        "💎 <b>Цурикавы</b> — стильный акриловый аксессуар для автомобиля.\n\n"
        "• Цена: <b>1800 ₽</b>\n"
        "• Материалы: зеркальный и матовый акрил\n"
        "• Толщина: 6 мм\n"
        "• Изготовление до 10 раб. дней\n\n"
        "👇 Вернуться в каталог можно ниже:",
        parse_mode="HTML",
        reply_markup=kb,
    )


# ---------- Стоимость ----------
@dp.callback_query(F.data == "price")
async def price(cb: types.CallbackQuery):
    await cb.message.edit_text(
        "💰 <b>Стоимость изделий</b>\n\n"
        "Эмблемы — 1200–2000 ₽\n"
        "Цурикавы — 1800 ₽\n"
        "Брелки — 800 ₽\n"
        "Подвески — 1400 ₽\n"
        "Колпачки — 1400 ₽ (комплект)\n"
        "Шильдики / надписи — от 800 ₽\n\n"
        "Для точного расчёта напишите менеджеру: @undercust_shop",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_start")]
        ])
    )


# ---------- Доставка ----------
@dp.callback_query(F.data == "delivery")
async def delivery(cb: types.CallbackQuery):
    await cb.message.edit_text(
        "🚚 <b>Доставка</b>\n\n"
        "📦 По России:\n"
        "• СДЭК — от 350 ₽\n"
        "• Яндекс.Доставка — от 300 ₽\n"
        "• Ozon Посылка — 99 ₽ 🎯\n\n"
        "🌍 В страны СНГ — СДЭК (от 700 ₽ / 10–25 дней)\n\n"
        "Отправка из Великого Новгорода.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_start")]
        ])
    )


# ---------- Назад ----------
@dp.callback_query(F.data == "back_start")
async def back_start(cb: types.CallbackQuery):
    await cb.message.edit_text(
        "Здесь можно:\n"
        "• посмотреть <b>примеры работ</b>,\n"
        "• узнать <b>стоимость</b> и <b>доставку</b>,\n"
        "• оформить <b>индивидуальный заказ</b>.\n\n"
        "Выбирай, что интересует 👇",
        parse_mode="HTML",
        reply_markup=main_menu(),
    )


# ---------- Запуск ----------
async def main():
    logging.info("Бот запускается...")
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка запуска: {e}")
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())