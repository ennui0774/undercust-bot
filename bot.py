# -*- coding: utf-8 -*-
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

# 🔐 Твой токен (замени, если создашь новый)
TOKEN = "7597289189:AAHwJUyLM99LIUm6hwFH52dxiO1GtnjPot4"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 📱 Главное меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📦 Каталог"), KeyboardButton(text="💬 Связаться с менеджером")],
        [KeyboardButton(text="🚚 Доставка"), KeyboardButton(text="💰 Стоимость")],
    ],
    resize_keyboard=True
)

# 📦 Меню каталога
catalog_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔗 Открыть каталог")],
        [KeyboardButton(text="🚘 Моей марки нет в каталоге")],
        [KeyboardButton(text="⬅️ Назад в меню")],
    ],
    resize_keyboard=True
)

# 💬 Меню после “моей марки нет…”
contact_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💬 Написать менеджеру")],
        [KeyboardButton(text="⬅️ Назад в меню")],
    ],
    resize_keyboard=True
)

# 🏁 /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! 👋 Я бот мастерской undercust.\n"
        "Выбери нужный раздел ниже 👇",
        reply_markup=main_menu
    )

# 📦 Каталог
@dp.message(F.text == "📦 Каталог")
async def catalog(message: types.Message):
    await message.answer(
        "📦 Каталог изделий undercust\n"
        "Вы можете открыть каталог или выбрать, если вашей марки нет 👇",
        reply_markup=catalog_menu
    )

# 🔗 Открыть каталог (ссылка ВКонтакте)
@dp.message(F.text == "🔗 Открыть каталог")
async def open_catalog(message: types.Message):
    await message.answer(
        "🛍 Вот ссылка на наш каталог во ВКонтакте:\n"
        "👉 https://vk.com/market-227792089?screen=group"
    )

# 🚘 Моей марки нет в каталоге
@dp.message(F.text == "🚘 Моей марки нет в каталоге")
async def no_brand(message: types.Message):
    await message.answer(
        "😔 К сожалению, пока что для вашей марки автомобиля не изготавливаем эмблему.\n\n"
        "Но вы можете уточнить возможность индивидуального заказа у менеджера 👇",
        reply_markup=contact_menu
    )

# 💬 Написать менеджеру
@dp.message(F.text == "💬 Написать менеджеру")
async def contact_from_no_brand(message: types.Message):
    await message.answer(
        "Свяжитесь с менеджером: @undercust_shop 💬",
        reply_markup=main_menu
    )

# ⬅️ Назад в меню
@dp.message(F.text == "⬅️ Назад в меню")
async def back_to_menu(message: types.Message):
    await message.answer(
        "Возвращаюсь в главное меню 👇",
        reply_markup=main_menu
    )

# 💬 Связаться с менеджером (из главного меню)
@dp.message(F.text == "💬 Связаться с менеджером")
async def contact(message: types.Message):
    await message.answer(
        "Напиши нашему менеджеру: @undercust_shop 💬"
    )

@dp.message(F.text == "🚚 Доставка")
async def delivery(message: types.Message):
    await message.answer(
        "🚚 <b>Доставка</b>\n\n"
        "<b>📦 По России:</b>\n"
        "• СДЭК — от 350 ₽ (доставка быстрее остальных)\n"
        "• Яндекс.Доставка — дешевле, но чуть дольше\n"
        "• Ozon Посылка — аналогично Яндекс.Доставке, сейчас акция: доставка за 99 ₽ 🎯\n\n"
        "<b>🌍 В страны СНГ:</b>\n"
        "• Только через СДЭК\n\n"
        "Для точного расчёта доставки обращайтесь к менеджеру: @undercust_shop 💬"
        , parse_mode="HTML"
    )


@dp.message(F.text == "💰 Стоимость")
async def pricing(message: types.Message):
    await message.answer(
        "💰 <b>Стоимость изделий</b>\n\n"
        "• Эмблемы — 1800 ₽ (есть исключения — очень маленькие, большие или со сложным дизайном)\n"
        "• Цурикавы — 1800 ₽\n"
        "• Брелки на ключи — 800 ₽\n"
        "• Подвески на зеркало — 1400 ₽\n"
        "• Накладки на колпачки в диски — 1400 ₽\n"
        "• Шильдики / надписи моделей — 800 ₽ (стоимость может меняться в зависимости от размеров и сложности)\n\n"
        "Для уточнения точной стоимости обращайтесь к менеджеру: @undercust_shop 💬"
        , parse_mode="HTML"
    )

# 🔁 Остальные сообщения
@dp.message()
async def fallback(message: types.Message):
    await message.answer(
        "Выбери пункт из меню ниже 👇",
        reply_markup=main_menu
    )

# 🚀 Запуск
async def main():
    print("Бот запущен ✅")
    # Отключаем webhook, если был активен
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

