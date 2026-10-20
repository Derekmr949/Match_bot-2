
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "matchbot.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                fixture_id INTEGER PRIMARY KEY,
                home_team TEXT NOT NULL,
                away_team TEXT NOT NULL,
                match_date TEXT,
                probability REAL NOT NULL,
                prediction TEXT NOT NULL,
                home_goals INTEGER,
                away_goals INTEGER,
                settled INTEGER NOT NULL DEFAULT 0
            )
        """)


def save_prediction(fixture_id, home_team, away_team,
                    match_date, probability):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO predictions (
                fixture_id, home_team, away_team,
                match_date, probability, prediction
            )
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(fixture_id) DO UPDATE SET
                probability = excluded.probability,
                prediction = excluded.prediction
        """, (
            fixture_id,
            home_team,
            away_team,
            match_date,
            probability,
            "Over 1.5"
        ))


def settle_prediction(fixture_id, home_goals, away_goals):
    with get_connection() as conn:
        conn.execute("""
            UPDATE predictions
            SET home_goals = ?,
                away_goals = ?,
                settled = 1
            WHERE fixture_id = ?
        """, (home_goals, away_goals, fixture_id))


def get_statistics():
    with get_connection() as conn:
        total = conn.execute("""
            SELECT COUNT(*) AS n
            FROM predictions
            WHERE settled = 1
        """).fetchone()["n"]

        wins = conn.execute("""
            SELECT COUNT(*) AS n
            FROM predictions
            WHERE settled = 1
              AND home_goals + away_goals >= 2
        """).fetchone()["n"]

    return {
        "settled": total,
        "wins": wins,
        "rate": round(wins / total * 100, 2) if total else 0
    }
