
from datetime import date, timedelta
import requests

from config import FOOTBALL_API_KEY, FOOTBALL_API_BASE_URL

SESSION = requests.Session()
SESSION.headers.update({
    "X-Auth-Token": FOOTBALL_API_KEY,
    "Accept": "application/json",
})


def api_get(path, params=None):
    url = f"{FOOTBALL_API_BASE_URL}/{path.lstrip('/')}"

    try:
        response = SESSION.get(
            url, params=params, timeout=20
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as exc:
        print(f"Erreur Football-Data.org : {exc}")
        return {}


def get_matches_for_date(match_date=None):
    match_date = match_date or date.today()
    data = api_get("matches", {
        "dateFrom": match_date.isoformat(),
        "dateTo": match_date.isoformat(),
    })
    return data.get("matches", [])


def get_team_history(team_id, before_date=None, limit=10):
    before_date = before_date or date.today()
    start_date = before_date - timedelta(days=180)

    data = api_get(f"teams/{team_id}/matches", {
        "dateFrom": start_date.isoformat(),
        "dateTo": (before_date - timedelta(days=1)).isoformat(),
        "status": "FINISHED",
        "limit": limit,
    })

    matches = data.get("matches", [])
    matches.sort(
        key=lambda match: match.get("utcDate", ""),
        reverse=True
    )
    return matches[:limit]


def get_match_results(match_date=None):
    matches = get_matches_for_date(match_date)
    return [
        match for match in matches
        if match.get("status") == "FINISHED"
    ]
