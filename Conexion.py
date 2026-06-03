import sqlite3
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = os.path.join(BASE_DIR, "bd", "biblioteca.db")
def getConexion():

    """Establece y devuelve la conexiÃ³n con la base de datos """
    try:
        return sqlite3.connect(URL)
    except sqlite3.OperationalError:
        print("Error al conectarse")
        raise