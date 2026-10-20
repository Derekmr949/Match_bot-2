
import os

TELEGRAM_BOT_TOKEN = os.getenv("8215985108:AAHzmAzepE9pSp1U-kU8Y-ZCPAFQgtMehzA", "")
FOOTBALL_API_KEY = os.getenv("f9c3fa644591453b9b7705722c57226e", "")

FOOTBALL_API_BASE_URL = "https://api.football-data.org/v4"

TIMEZONE = "Africa/Lubumbashi"

# Seuil de tri, pas une garantie de réussite.
MIN_OVER_15_PROBABILITY = 75
MAX_DAILY_MATCHES = 8

# Codes de compétitions à analyser.
# Les matchs réellement accessibles dépendent de ton offre API.
COMPETITIONS = [
    "PL",   # Premier League
    "PD",   # Liga
    "BL1",  # Bundesliga
    "SA",   # Serie A
    "FL1",  # Ligue 1
    "CL",   # Ligue des champions
]


def validate_config():
    missing = []

    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")

    if not FOOTBALL_API_KEY:
        missing.append("FOOTBALL_API_KEY")

    if missing:
        raise RuntimeError(
            "Variables manquantes : " + ", ".join(missing)
        )
