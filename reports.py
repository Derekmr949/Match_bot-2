
from datetime import datetime
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Africa/Lubumbashi")


def format_report(predictions):
    now = datetime.now(TZ).strftime("%d/%m/%Y %H:%M")

    if not predictions:
        return (
            "⚽ MATCHBOT — OVER 1,5\n\n"
            f"Rapport du {now}\n\n"
            "Aucun match n'a passé le filtre aujourd'hui.\n"
            "Cela ne signifie pas qu'il n'y a aucun match."
        )

    lines = [
        "⚽ MATCHBOT — OVER 1,5 BUTS",
        f"Rapport : {now}",
        "",
        "Estimations statistiques, non garanties.",
        "",
    ]

    for index, item in enumerate(predictions, 1):
        kickoff = item.get("date", "")
        try:
            kickoff_dt = datetime.fromisoformat(
                kickoff.replace("Z", "+00:00")
            ).astimezone(TZ)
            kickoff = kickoff_dt.strftime("%H:%M")
        except (ValueError, TypeError):
            kickoff = "heure inconnue"

        lines.extend([
            f"{index}. {item['home_team']} - {item['away_team']}",
            f"   Heure (Lubumbashi) : {kickoff}",
            f"   Over 1,5 estimé : {item['probability']} %",
            f"   Total de buts attendu : {item['expected_goals']}",
            "",
        ])

    lines.append("Parie de façon responsable.")
    return "\n".join(lines)
