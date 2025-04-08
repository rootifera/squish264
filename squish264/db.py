import sqlite3

from squish264.config import DATABASE_PATH
from squish264.utils import log


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def init_db():
    with get_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY,
                original_path TEXT UNIQUE,
                output_path TEXT,
                status TEXT,
                last_modified_time REAL
            )
        ''')
    log("Database initialised", "OK")


def add_file(original_path, output_path, last_modified_time):
    with get_connection() as conn:
        conn.execute('''
            INSERT OR IGNORE INTO files (original_path, output_path, status, last_modified_time)
            VALUES (?, ?, 'found', ?)
        ''', (original_path, output_path, last_modified_time))


def update_status(original_path, status):
    with get_connection() as conn:
        conn.execute('''
            UPDATE files SET status = ? WHERE original_path = ?
        ''', (status, original_path))


def get_files_by_status(status):
    with get_connection() as conn:
        cur = conn.execute('''
            SELECT original_path, output_path FROM files WHERE status = ?
        ''', (status,))
        return cur.fetchall()
