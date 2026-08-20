import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# =========================
# НАСТРОЙКИ
# =========================

TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("Не задан BOT_TOKEN")

# =========================
# WEB-СЕРВЕР ДЛЯ RENDER
# =========================

app = Flask(__name__)

@app.route("/")
def home():
    return "Работа CPS Bot работает!"

@app.route("/health")
def health():
    return "OK"


def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


# =========================
# КЛАВИАТУРЫ
# =========================

def main_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🔎 Найти работу", callback_data="search")
        ],
        [
            InlineKeyboardButton("🔔 Мои подписки", callback_data="subscribe")
        ],
        [
            InlineKeyboardButton("🏢 Разместить вакансию", callback_data="employer")
        ],
        [
            InlineKeyboardButton("ℹ️ О боте", callback_data="about")
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def locations_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("📍 Чехов", callback_data="city_chekhov")
        ],
        [
            InlineKeyboardButton("📍 Подольск", callback_data="city_podolsk")
        ],
        [
            InlineKeyboardButton("📍 Серпухов", callback_data="city_serpukhov")
        ],
        [
            InlineKeyboardButton("🏠 Удалённая работа", callback_data="remote")
        ],
        [
            InlineKeyboardButton("⬅️ Назад", callback_data="back")
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================
# /START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "👋 <b>Работа CPS</b>\n\n"
        "Вакансии Чехова, Подольска и Серпухова.\n\n"
        "Здесь мы будем собирать вакансии "
        "от работодателей и с сайтов поиска работы.\n\n"
        "Выберите действие:"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=main_keyboard()
    )


# =========================
# ОБРАБОТКА КНОПОК
# =========================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    if query.data == "search":

        await query.edit_message_text(
            "🔎 <b>Где ищем работу?</b>\n\n"
            "Выберите город или удалённую работу:",
            parse_mode="HTML",
            reply_markup=locations_keyboard()
        )

    elif query.data == "city_chekhov":

        await query.edit_message_text(
            "📍 <b>Чехов</b>\n\n"
            "Пока база вакансий пуста.\n\n"
            "Следующим этапом подключим автоматический "
            "поиск вакансий и будем показывать здесь "
            "свежие предложения.",
            parse_mode="HTML",
            reply_markup=main_keyboard()
        )

    elif query.data == "city_podolsk":

        await query.edit_message_text(
            "📍 <b>Подольск</b>\n\n"
            "Пока база вакансий пуста.\n\n"
            "Скоро здесь появятся свежие вакансии.",
            parse_mode="HTML",
            reply_markup=main_keyboard()
        )

    elif query.data == "city_serpukhov":

        await query.edit_message_text(
            "📍 <b>Серпухов</b>\n\n"
            "Пока база вакансий пуста.\n\n"
            "Скоро здесь появятся свежие вакансии.",
            parse_mode="HTML",
            reply_markup=main_keyboard()
        )

    elif query.data == "remote":

        await query.edit_message_text(
            "🏠 <b>Удалённая работа</b>\n\n"
            "Пока база вакансий пуста.\n\n"
