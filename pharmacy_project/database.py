import sqlite3
import os
from datetime import datetime

DB = "hospital.db"


def get_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def query(q, args=(), one=False):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(q, args)
    conn.commit()
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv


def init_db():
    # Якщо база вже існує — нічого не створюємо
    if os.path.exists(DB):
        return

    conn = get_connection()
    cur = conn.cursor()

    # USERS
    cur.execute("""
    CREATE TABLE users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
    )
    """)

    departments = [
        "поліклініка","приймальне","педіатрія","інфекція",
        "терапія","неврологія","гінекологія","хірургія","ВАІТ"
    ]

    cur.execute("INSERT INTO users VALUES(NULL,'склад','1234','warehouse')")
    for d in departments:
        cur.execute("INSERT INTO users VALUES(NULL,?,?,?)",(d,d,"department"))

    # MEDICINES
    cur.execute("""
    CREATE TABLE medicines(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    """)

    # BATCHES (партії)
    cur.execute("""
    CREATE TABLE batches(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medicine_id INTEGER,
        series TEXT,
        expiry TEXT,
        quantity INTEGER
    )
    """)

    # RESERVATIONS
    cur.execute("""
    CREATE TABLE reservations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        department TEXT,
        status TEXT,
        created TEXT,
        confirmed_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE reservation_items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reservation_id INTEGER,
        medicine_id INTEGER,
        quantity INTEGER
    )
    """)

    # MOVEMENT LOG
    cur.execute("""
    CREATE TABLE movement_log(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medicine_id INTEGER,
        change INTEGER,
        type TEXT,
        created TEXT
    )
    """)

    conn.commit()
    conn.close()