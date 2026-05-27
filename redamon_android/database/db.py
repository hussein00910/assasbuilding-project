"""database/db.py — SQLite persistence layer."""
import sqlite3, os
from datetime import datetime

DB_PATH = os.path.join(os.path.expanduser('~'), 'redamon.db')


def _conn():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c


def init_db():
    with _conn() as c:
        c.executescript('''
            CREATE TABLE IF NOT EXISTS scans (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                target   TEXT NOT NULL,
                created  TEXT NOT NULL,
                status   TEXT DEFAULT 'running',
                risk     TEXT DEFAULT 'Unknown',
                summary  TEXT DEFAULT ''
            );
            CREATE TABLE IF NOT EXISTS findings (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id  INTEGER NOT NULL,
                tool     TEXT NOT NULL,
                severity TEXT DEFAULT 'INFO',
                title    TEXT NOT NULL,
                detail   TEXT NOT NULL,
                created  TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS raw_output (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id  INTEGER NOT NULL,
                tool     TEXT NOT NULL,
                output   TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS conversations (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id  INTEGER,
                role     TEXT NOT NULL,
                content  TEXT NOT NULL,
                created  TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS settings (
                key      TEXT PRIMARY KEY,
                value    TEXT NOT NULL
            );
        ''')

# ── Scans ────────────────────────────────────────────────────────────────────
def create_scan(target: str) -> int:
    with _conn() as c:
        cur = c.execute(
            'INSERT INTO scans (target, created) VALUES (?,?)',
            (target, datetime.now().isoformat())
        )
        return cur.lastrowid


def update_scan(scan_id, **kw):
    allowed = {'status', 'risk', 'summary'}
    fields = {k: v for k, v in kw.items() if k in allowed}
    if not fields:
        return
    sql = 'UPDATE scans SET ' + ','.join(f'{k}=?' for k in fields) + ' WHERE id=?'
    with _conn() as c:
        c.execute(sql, list(fields.values()) + [scan_id])


def get_scans(limit=30):
    with _conn() as c:
        return c.execute(
            'SELECT * FROM scans ORDER BY created DESC LIMIT ?', (limit,)
        ).fetchall()


def get_scan(scan_id):
    with _conn() as c:
        return c.execute('SELECT * FROM scans WHERE id=?', (scan_id,)).fetchone()


def delete_scan(scan_id):
    with _conn() as c:
        c.execute('DELETE FROM scans    WHERE id=?',      (scan_id,))
        c.execute('DELETE FROM findings WHERE scan_id=?', (scan_id,))
        c.execute('DELETE FROM raw_output WHERE scan_id=?', (scan_id,))
        c.execute('DELETE FROM conversations WHERE scan_id=?', (scan_id,))


# ── Findings ─────────────────────────────────────────────────────────────────
def save_finding(scan_id, tool, severity, title, detail):
    with _conn() as c:
        c.execute(
            'INSERT INTO findings (scan_id,tool,severity,title,detail,created) VALUES (?,?,?,?,?,?)',
            (scan_id, tool, severity, title, detail, datetime.now().isoformat())
        )


def get_findings(scan_id):
    with _conn() as c:
        return c.execute(
            'SELECT * FROM findings WHERE scan_id=? ORDER BY '
            "CASE severity WHEN 'CRITICAL' THEN 0 WHEN 'HIGH' THEN 1 "
            "WHEN 'MEDIUM' THEN 2 WHEN 'LOW' THEN 3 ELSE 4 END",
            (scan_id,)
        ).fetchall()


def save_raw(scan_id, tool, output):
    with _conn() as c:
        c.execute(
            'INSERT INTO raw_output (scan_id,tool,output) VALUES (?,?,?)',
            (scan_id, tool, output)
        )


def get_raw(scan_id):
    with _conn() as c:
        return c.execute(
            'SELECT * FROM raw_output WHERE scan_id=?', (scan_id,)
        ).fetchall()


# ── Conversations ─────────────────────────────────────────────────────────────
def save_msg(scan_id, role, content):
    with _conn() as c:
        c.execute(
            'INSERT INTO conversations (scan_id,role,content,created) VALUES (?,?,?,?)',
            (scan_id, role, content, datetime.now().isoformat())
        )


def get_conv(scan_id):
    with _conn() as c:
        return c.execute(
            'SELECT * FROM conversations WHERE scan_id=? ORDER BY created',
            (scan_id,)
        ).fetchall()


# ── Settings ─────────────────────────────────────────────────────────────────
def set_cfg(key, value):
    with _conn() as c:
        c.execute('INSERT OR REPLACE INTO settings (key,value) VALUES (?,?)', (key, value))


def get_cfg(key, default=''):
    with _conn() as c:
        row = c.execute('SELECT value FROM settings WHERE key=?', (key,)).fetchone()
        return row['value'] if row else default
