
import asyncio
import logging
import os
import threading
from datetime import datetime
from zoneinfo import ZoneInfo

from flask import Flask, jsonify
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from config import TELEGRAM_BOT_TOKEN, validate_config
from database import init_db, save_prediction
from reports import format_report
from selector import select_matches
from statistics import build_statistics_report

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TZ = ZoneInfo("Africa/Lubumbashi")
web = Flask(__name__)


@web.get("/")
def health():
    return jsonify({"service": "MatchBot", "status": "ok"})


@web.get("/health")
def health_check():
    return jsonify({"status": "healthy"})


async def start_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "⚽ Bienvenue sur MatchBot !\n\n"
        "/today — Pronostics Over 1,5 du jour\n"
        "/stats — Statistiques enregistrées\n\n"
        "Les estimations ne sont jamais garanties."
    )


async def today_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "🔎 Analyse des matchs en cours. Patiente un instant..."
    )

    try:
        today = datetime.now(TZ).date()
        predictions = await asyncio.to_thread(
            select_matches, today
        )

        for item in predictions:
            if item.get("fixture_id") is not None:
                save_prediction(
                    item["fixture_id"],
                    item["home_team"],
                    item["away_team"],
                    item["date"],
                    item["probability"],
                )

        await update.message.reply_text(
            format_report(predictions)
        )

    except Exception:
        logger.exception("Erreur pendant /today")
        await update.message.reply_text(
            "Une erreur est survenue pendant l'analyse. "
            "Vérifie les journaux Render et l'accès à l'API."
        )


async def stats_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        build_statistics_report()
    )


async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):
    logger.error(
        "Erreur Telegram : %s",
        context.error,
    )


def run_web_server():
    port = int(os.environ.get("PORT", "10000"))
    web.run(
        host="0.0.0.0",
        port=port,
        use_reloader=False,
    )


def main():
    validate_config()
    init_db()

    threading.Thread(
        target=run_web_server,
        daemon=True,
    ).start()

    application = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start_command)
    )
    application.add_handler(
        CommandHandler("today", today_command)
    )
    application.add_handler(
        CommandHandler("stats", stats_command)
    )
    application.add_error_handler(error_handler)

    logger.info("MatchBot démarre...")
    application.run_polling()


if __name__ == "__main__":
    main()
