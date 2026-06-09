"""
SQLite storage for scan history and saved results.
"""

import sqlite3
import os
from datetime import datetime

# Determine writable path (works on Android and desktop)
try:
    from android.storage import app_storage_path  # type: ignore
    DB_DIR = app_storage_path()
except ImportError:
    DB_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, 'history.db')


def _conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    """Create tables if they don't exist."""
    with _conn() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                ts       TEXT NOT NULL,
                category TEXT NOT NULL,
                tool     TEXT NOT NULL,
                target   TEXT NOT NULL,
                output   TEXT NOT NULL
            )
        """)
        con.commit()


def save_result(category: str, tool: str, target: str, output: str):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with _conn() as con:
        con.execute(
            "INSERT INTO history (ts, category, tool, target, output) VALUES (?,?,?,?,?)",
            (ts, category, tool, target, output[:8000])
        )
        con.commit()


def get_history(limit: int = 50):
    """Return list of dicts, newest first."""
    with _conn() as con:
        cur = con.execute(
            "SELECT id, ts, category, tool, target, output FROM history ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        rows = cur.fetchall()
    return [
        {'id': r[0], 'ts': r[1], 'category': r[2],
         'tool': r[3], 'target': r[4], 'output': r[5]}
        for r in rows
    ]


def delete_all():
    with _conn() as con:
        con.execute("DELETE FROM history")
        con.commit()
