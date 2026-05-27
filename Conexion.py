import sqlite3

def getconexion():
    conn=sqlite3.connect("biblioteca.db")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS biblioteca (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT
    )
    """)
    conn.commit()
    conn.close()
