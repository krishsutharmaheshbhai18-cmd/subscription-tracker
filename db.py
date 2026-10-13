"""
db.py - all database code lives here (SQLite, a simple file-based database).

Table: subscriptions
  id            - unique number for each row
  name          - "Netflix", "Spotify", etc.
  price         - amount per billing cycle
  cycle         - "monthly" or "yearly"
  category      - "Streaming", "Education", "Tools", etc.
  renewal_date  - next date it charges (YYYY-MM-DD)
  last_used     - date you last used it (user updates this manually) - used for
                  the "you haven't opened this in a while" insight
"""
import sqlite3
from datetime import date

DB_PATH = "subscriptions.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    return conn


def init_db():
    """Create the table if it doesn't exist yet. Call this once at app startup."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            cycle TEXT NOT NULL,
            category TEXT NOT NULL,
            renewal_date TEXT NOT NULL,
            last_used TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_subscription(name, price, cycle, category, renewal_date, last_used=None):
    conn = get_connection()
    conn.execute(
        "INSERT INTO subscriptions (name, price, cycle, category, renewal_date, last_used) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (name, price, cycle, category, renewal_date, last_used or str(date.today())),
    )
    conn.commit()
    conn.close()


def get_all():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM subscriptions ORDER BY renewal_date").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_subscription(sub_id):
    conn = get_connection()
    conn.execute("DELETE FROM subscriptions WHERE id = ?", (sub_id,))
    conn.commit()
    conn.close()


def mark_used_today(sub_id):
    conn = get_connection()
    conn.execute("UPDATE subscriptions SET last_used = ? WHERE id = ?",
                 (str(date.today()), sub_id))
    conn.commit()
    conn.close()


def monthly_total():
    """Convert everything to a monthly equivalent and sum it up."""
    subs = get_all()
    total = 0.0
    for s in subs:
        total += s["price"] if s["cycle"] == "monthly" else s["price"] / 12
    return round(total, 2)
