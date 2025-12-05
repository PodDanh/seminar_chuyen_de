import sqlite3
from typing import List, Tuple, Dict

DB_PATH = "sentiments.db"


def get_connection():
    #check_same_thread=False để dùng được trong Streamlit
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sentiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            score REAL NOT NULL,
            timestamp TEXT NOT NULL
        );
        """
    )
    conn.commit()
    conn.close()


def insert_sentiment(record: Dict):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO sentiments (text, sentiment, score, timestamp) VALUES (?, ?, ?, ?)",
        (record["text"], record["sentiment"], record["score"], record["timestamp"]),
    )
    conn.commit()
    conn.close()


def get_latest(limit: int = 50) -> List[Tuple]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, text, sentiment, score, timestamp "
        "FROM sentiments ORDER BY timestamp DESC LIMIT ?",
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows

def clear_history():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM sentiments")
    conn.commit()
    conn.close()
