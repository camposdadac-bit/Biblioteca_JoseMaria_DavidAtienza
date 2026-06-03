import os
import sqlite3

def ejecutar_script_sql():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SQL_FILE = os.path.join(BASE_DIR, "bd", "biblioteca.sql")
    DB_FILE = os.path.join(BASE_DIR, "bd", "biblioteca.db")

    conn = sqlite3.connect(DB_FILE, isolation_level=None)
    cursor = conn.cursor()

    try:
        with open(SQL_FILE, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        cursor.executescript(sql_script)

    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo en {SQL_FILE}")
    except sqlite3.Error as e:
        print(f"❌ Error de SQLite durante la transacción: {e}")

    finally:
        conn.close()


if __name__ == "__main__":
    ejecutar_script_sql()