import sqlite3
from datetime import datetime

DB_PATH = "user_data.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT
                )""")
    c.execute("""CREATE TABLE IF NOT EXISTS translations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    paragraph TEXT,
                    user_translation TEXT,
                    reference_translation TEXT,
                    similarity REAL,
                    timestamp TEXT
                )""")
    c.execute("""CREATE TABLE IF NOT EXISTS wordbook (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    word TEXT,
                    note TEXT,
                    timestamp TEXT
                )""")
    conn.commit()
    conn.close()

# ========== USER OPERATIONS ==========
def add_user(username, password):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def get_user(username, password):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user

# ========== TRANSLATION OPERATIONS ==========
def save_translation(user_id, paragraph, user_translation, ref_translation, similarity):
    conn = get_conn()
    c = conn.cursor()
    # aynı paragraf varsa güncelle
    c.execute("SELECT id FROM translations WHERE user_id=? AND paragraph=?", (user_id, paragraph))
    existing = c.fetchone()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if existing:
        c.execute("""
            UPDATE translations SET user_translation=?, similarity=?, timestamp=? WHERE id=?
        """, (user_translation, similarity, now, existing[0]))
    else:
        c.execute("""
            INSERT INTO translations (user_id, paragraph, user_translation, reference_translation, similarity, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, paragraph, user_translation, ref_translation, similarity, now))
    conn.commit()
    conn.close()

def get_translations(user_id):
    conn = get_conn()
    c = conn.cursor()
    rows = c.execute("""
        SELECT paragraph, user_translation, reference_translation, similarity, timestamp, id
        FROM translations
        WHERE user_id=?
        ORDER BY id DESC
    """, (user_id,)).fetchall()
    conn.close()
    return rows



# ========== WORDBOOK ==========
def add_word(user_id, word, note):
    conn = get_conn()
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO wordbook (user_id, word, note, timestamp) VALUES (?, ?, ?, ?)",
              (user_id, word, note, now))
    conn.commit()
    conn.close()

def get_wordbook(user_id):
    conn = get_conn()
    c = conn.cursor()
    rows = c.execute("""
        SELECT word, note, timestamp FROM wordbook WHERE user_id=? ORDER BY id DESC
    """, (user_id,)).fetchall()
    conn.close()
    return rows

def delete_translation(translation_id, user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM translations WHERE id=? AND user_id=?", (translation_id, user_id))
    conn.commit()
    conn.close()
