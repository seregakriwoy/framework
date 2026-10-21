import sqlite3

DB_PATH = "data/supply_manager.sqlite"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    # Включаем поддержку внешних ключей
    conn.execute("PRAGMA foreign_keys = ON")
    # Позволяет обращаться к полям по именам (row['name'])
    conn.row_factory = sqlite3.Row
    return conn