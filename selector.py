
from datetime import datetime, timezone

from config import MIN_OVER_15_PROBABILITY, MAX_DAILY_MATCHES
from football_api import get_matches_for_date, get_team_history
from predictor import predict_match


def select_matches(match_date=None):
    matches = get_matches_for_date(match_date)
    selected = []

    for match in matches:
        if match.get("status") not in ("TIMED", "SCHEDULED"):
            continue

        home_id = match.get("homeTeam", {}).get("id")
        away_id = match.get("awayTeam", {}).get("id")

        if not home_id or not away_id:
            continue

        kickoff = match.get("utcDate", "")
        try:
            kickoff_date = datetime.fromisoformat(
                kickoff.replace("Z", "+00:00")
            ).date()
            reference_date = match_date or datetime.now(
                timezone.utc
            ).date()

            if kickoff_date < reference_date:
                continue
        except ValueError:
            pass

        home_history = get_team_history(home_id)
        away_history = get_team_history(away_id)

        prediction = predict_match(
            match, home_history, away_history
        )

        if not prediction:
            continue

        if prediction["probability"] >= MIN_OVER_15_PROBABILITY:
            selected.append(prediction)

    selected.sort(
        key=lambda item: item["probability"],
        reverse=True
    )

    return selected[:MAX_DAILY_MATCHES]
