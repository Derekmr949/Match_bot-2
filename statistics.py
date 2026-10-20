
from database import get_statistics


def build_statistics_report():
    stats = get_statistics()

    if stats["settled"] == 0:
        return (
            "📊 STATISTIQUES MATCHBOT\n\n"
            "Aucun pronostic réglé pour le moment.\n"
            "Les résultats seront évalués après les matchs."
        )

    losses = stats["settled"] - stats["wins"]

    return (
        "📊 STATISTIQUES MATCHBOT\n\n"
        f"Pronostics évalués : {stats['settled']}\n"
        f"Over 1,5 réussi : {stats['wins']}\n"
        f"Over 1,5 échoué : {losses}\n"
        f"Taux de réussite observé : {stats['rate']} %\n\n"
        "Les performances passées ne garantissent pas "
        "les performances futures."
    )
