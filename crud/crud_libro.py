import sqlite3
from pathlib import Path
from DTO.Libro import Libro

RUTA_BD = Path(__file__).resolve().parent.parent / "bd" / "biblioteca.db"


def insertar_en_bd(titulo, autor, disponible, isbn):
    """Inserta una nueva fila en la base de datos y devuelve el ID generado."""
    val_disponible = 1 if disponible else 0
    with sqlite3.connect(RUTA_BD) as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO libros (titulo, autor, disponible, isbn) VALUES (?, ?, ?, ?)",
            (titulo, autor, val_disponible, isbn)
        )
        conexion.commit()
        return cursor.lastrowid


def seleccionar_por_id(id_libro):
    """Busca una fila por ID y la transforma en un objeto Libro."""
    with sqlite3.connect(RUTA_BD) as conexion:
        fila = conexion.execute(
            "SELECT id, titulo, autor, disponible, isbn FROM libros WHERE id = ?", (id_libro,)
        ).fetchone()
    if fila:
        return Libro(fila[0], fila[1], fila[2], bool(fila[3]), fila[4])
    return None


def seleccionar_todos():
    """Trae todas las filas de la tabla libros de la base de datos."""
    with sqlite3.connect(RUTA_BD) as conexion:
        filas = conexion.execute("SELECT id, titulo, autor, disponible, isbn FROM libros").fetchall()

    lista = []
    for f in filas:
        lista.append(Libro(f[0], f[1], f[2], bool(f[3]), f[4]))
    return lista


def modificar_en_bd(id_libro, titulo, autor, disponible, isbn):
    """Actualiza los datos de un libro existente en la base de datos."""
    val_disponible = 1 if disponible else 0
    with sqlite3.connect(RUTA_BD) as conexion:
        conexion.execute(
            "UPDATE libros SET titulo = ?, autor = ?, disponible = ?, isbn = ? WHERE id = ?",
            (titulo, autor, val_disponible, isbn, id_libro)
        )
        conexion.commit()


def borrar_de_bd(id_libro):
    """Elimina permanentemente la fila de un libro usando su ID."""
    with sqlite3.connect(RUTA_BD) as conexion:
        conexion.execute("DELETE FROM libros WHERE id = ?", (id_libro,))
        conexion.commit()