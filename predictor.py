
import math


def match_goals(match):
    score = match.get("score", {}).get("fullTime", {})
    home = score.get("home")
    away = score.get("away")

    if home is None or away is None:
        return None

    return home, away


def team_goal_averages(history, team_id):
    scored = []
    conceded = []

    for match in history:
        goals = match_goals(match)
        if goals is None:
            continue

        home_id = match.get("homeTeam", {}).get("id")
        away_id = match.get("awayTeam", {}).get("id")
        home_goals, away_goals = goals

        if home_id == team_id:
            scored.append(home_goals)
            conceded.append(away_goals)
        elif away_id == team_id:
            scored.append(away_goals)
            conceded.append(home_goals)

    if not scored:
        return 1.2, 1.2

    return sum(scored) / len(scored), sum(conceded) / len(conceded)


def probability_over_15(expected_goals):
    # Modèle de Poisson : P(total >= 2) = 1 - P(0) - P(1)
    if expected_goals <= 0:
        return 0.0

    probability = 1 - math.exp(-expected_goals) * (
        1 + expected_goals
    )

    return round(max(0, min(1, probability)) * 100, 1)


def predict_match(match, home_history, away_history):
    home_id = match.get("homeTeam", {}).get("id")
    away_id = match.get("awayTeam", {}).get("id")

    if not home_id or not away_id:
        return None

    home_scored, home_conceded = team_goal_averages(
        home_history, home_id
    )
    away_scored, away_conceded = team_goal_averages(
        away_history, away_id
    )

    expected_home = (home_scored + away_conceded) / 2
    expected_away = (away_scored + home_conceded) / 2

    expected_total = expected_home + expected_away

    return {
        "fixture_id": match.get("id"),
        "home_team": match.get("homeTeam", {}).get("name", "?"),
        "away_team": match.get("awayTeam", {}).get("name", "?"),
        "date": match.get("utcDate", ""),
        "expected_goals": round(expected_total, 2),
        "probability": probability_over_15(expected_total),
        "market": "Over 1.5 buts",
    }
