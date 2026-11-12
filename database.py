import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "krishimitra.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer_name TEXT,
                village TEXT,
                crop TEXT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                mode TEXT,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()

def save_interaction(farmer_name, village, crop, question, answer, mode):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO interactions
            (farmer_name, village, crop, question, answer, mode, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            farmer_name, village, crop, question, answer, mode,
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ))
        conn.commit()

def get_recent_interactions(limit=8):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT farmer_name, village, crop, question, answer, mode, created_at
        FROM interactions
        ORDER BY id DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]
