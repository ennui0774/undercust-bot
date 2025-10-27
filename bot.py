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
from aiogram.exceptions import TelegramConflictError

# 🔐 Токен
TOKEN = os.getenv("TOKEN") or "7597289189:AAFxpew7hKcxO9xLOUCOkAxmJa5zUqntlLM"

# 🧠 Логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

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
        if getattr(message, "photo", None):
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
        "<b>Эмблемы:</b>\n"
        "• Маленькие — <b>от 1200 до 1600 ₽</b>\n"
        "• Средние — <b>1800 ₽</b> <i>(таких около 90% всех заказов)</i>\n"
        "• Большие или сложные дизайны — <b>от 2000 ₽</b>\n"
        "➕ При покупке <b>двух эмблем — скидка 400 ₽</b>\n"
        "Например: 1800 + 1800 = 3600 ₽ → <b>3200 ₽</b>\n\n"
        "<b>Цурикавы:</b>\n"
        "от <b>1600 ₽</b> до <b>1800 ₽</b>\n\n"
        "<b>Подвески на зеркало:</b>\n"
        "<b>1400 ₽</b>\n\n"
        "<b>Накладки на колпачки ступиц:</b>\n"
        "<b>1400 ₽ за комплект</b>\n\n"
        "<b>Брелки:</b>\n"
        "<b>800 ₽</b>\n\n"
        "<b>Шильдики (надписи):</b>\n"
        "от <b>800 ₽</b> — в зависимости от размера и сложности"
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
        [InlineKeyboardButton(text="💳 Оплата", callback_data="faq_payment")],
        [InlineKeyboardButton(text="⏱ Сроки изготовления", callback_data="faq_terms")],
        [InlineKeyboardButton(text="🚀 Срочное изготовление", callback_data="faq_fast")],
        [InlineKeyboardButton(text="🎨 Индивидуальный дизайн", callback_data="faq_design")],
        [InlineKeyboardButton(text="📎 Крепление эмблемы", callback_data="faq_mount")],
        [InlineKeyboardButton(text="🔩 Материалы", callback_data="faq_materials")],
        [InlineKeyboardButton(text="💎 Гравировка", callback_data="faq_engraving")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_start")]
    ])
    await safe_edit(callback.message, text, parse_mode="HTML", reply_markup=kb)


faq_answers = {
    "faq_order": (
        "🛠 <b>Как оформить заказ?</b>\n\n"
        "Вы можете выбрать готовый дизайн из каталога или заказать индивидуальный макет. "
        "Если создаётся новый дизайн — учтём все пожелания по <b>цветам, размерам, гравировке и стилю</b>.\n\n"
        "После согласования макета уточняем возможность установки эмблемы, формируем согласование, "
        "беру предоплату и запускаю в производство. После изготовления отправляю фото/видео готового заказа, "
        "после чего оплачивается оставшаяся сумма и доставка."
    ),
    "faq_payment": (
        "💳 <b>Как происходит оплата?</b>\n\n"
        "Оплата проходит в два этапа:\n"
        "• после утверждения макета — <b>предоплата</b> "
        "(500 ₽ для заказов до 4000 ₽ / 1000 ₽ для заказов от 4000 ₽);\n"
        "• после изготовления — <b>остаток суммы + доставка</b>.\n\n"
        "Если доставка <b>СДЭКом</b> — оплачивается при получении. "
        "Если <b>Ozon</b> или <b>Яндекс.Доставка</b> — оплачивается сразу при отправке."
    ),
    "faq_terms": (
        "⏱ <b>Какие сроки изготовления?</b>\n\n"
        "Обычно до 10 рабочих дней (в зависимости от загруженности). "
        "Если нужно срочно — см. пункт «🚀 Срочное изготовление»."
    ),
    "faq_fast": (
        "🚀 <b>Можно ли изготовить быстрее?</b>\n\n"
        "Да, если нужно срочно — например, к дню рождения или в подарок. "
        "Есть услуга <b>срочного изготовления</b>: заказ изготавливается и отправляется в течение 2 дней. "
        "Доплата составляет 750 ₽ для небольших изделий, для крупных рассчитывается индивидуально."
    ),
    "faq_design": (
        "🎨 <b>Можно ли сделать индивидуальный дизайн?</b>\n\n"
        "Да, конечно — на этом и специализируется мастерская. "
        "Напишите менеджеру 👉 <a href='https://t.me/undercust_shop'>@undercust_shop</a>"
    ),
    "faq_mount": (
        "📎 <b>Как крепится эмблема?</b>\n\n"
        "На заднюю поверхность каждой эмблемы нанесён прочный <b>3М-скотч</b>. "
        "Перед установкой нужно тщательно очистить место, обезжирить и приклеить на тёплую поверхность. "
        "Если площадка немного изогнута — пластик можно аккуратно прогреть феном, чтобы придать форму."
    ),
    "faq_materials": (
        "🔩 <b>Из чего изготавливаются изделия?</b>\n\n"
        "Используется <b>качественное цветное оргстекло</b> — прочное, гибкое и долговечное. "
        "Крепление — оригинальный <b>3М-скотч</b>, обеспечивающий надёжную фиксацию."
    ),
    "faq_engraving": (
        "💎 <b>Что такое гравировка?</b>\n\n"
        "Гравировка выполняется лазером по акрилу — не выцветает, не облезает и остаётся навсегда. "
        "Это эстетичная, аккуратная и <b>вечная деталь изделия</b>."
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
        webhook_info = await bot.get_webhook_info()
        if webhook_info.url:
            logging.warning(f"Найден активный webhook: {webhook_info.url} — удаляю...")
            await bot.delete_webhook(drop_pending_updates=True)
            await asyncio.sleep(1)
    except Exception as e:
        logging.warning(f"Ошибка при проверке webhook: {e}")

    while True:
        try:
            await dp.start_polling(bot)
        except TelegramConflictError:
            logging.warning("Обнаружен конфликт polling — жду 10 секунд и пробую снова...")
            await asyncio.sleep(10)
        except Exception as e:
            logging.error(f"Ошибка в polling: {e}")
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
