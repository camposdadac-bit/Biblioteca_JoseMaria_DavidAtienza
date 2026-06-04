import sqlite3
from pathlib import Path
from DTO.Libro import Libro

RUTA_BD = Path(__file__).resolve().parent.parent / "bd" / "biblioteca.db"

class DAO_libro:
    @staticmethod
    def insertar_en_bd(titulo, autor, disponible, isbn):
        """Inserta una nueva fila en la base de datos y devuelve el ID generado"""
        val_disponible = 1 if disponible else 0
        conexion = sqlite3.connect(RUTA_BD, timeout=10.0)
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO libros (titulo, autor, disponible, isbn) VALUES (?, ?, ?, ?)",
                (titulo, autor, val_disponible, isbn)
            )
            conexion.commit()
            return cursor.lastrowid
        finally:
            conexion.close()

    @staticmethod
    def seleccionar_por_id(id_libro):
        """Busca una fila por ID y la transforma en un objeto Libro"""
        conexion = sqlite3.connect(RUTA_BD, timeout=10.0)
        try:
            fila = conexion.execute(
                "SELECT id, titulo, autor, disponible, isbn FROM libros WHERE id = ?", (id_libro,)
            ).fetchone()
        finally:
            conexion.close()
        if fila:
            return Libro(fila[0], fila[1], fila[2], bool(fila[3]), fila[4])
        return None

    @staticmethod
    def seleccionar_todos():
        """Trae todas las filas de la tabla libros de la base de datos"""
        conexion = sqlite3.connect(RUTA_BD, timeout=10.0)
        try:
            filas = conexion.execute("SELECT id, titulo, autor, disponible, isbn FROM libros").fetchall()
        finally:
            conexion.close()
        lista = []
        for f in filas:
            lista.append(Libro(f[0], f[1], f[2], bool(f[3]), f[4]))
        return lista

    @staticmethod
    def modificar_en_bd(id_libro, titulo, autor, disponible, isbn):
        """Actualiza los datos de un libro existente en la base de datos"""
        val_disponible = 1 if disponible else 0
        conexion = sqlite3.connect(RUTA_BD, timeout=10.0)
        try:
            conexion.execute(
                "UPDATE libros SET titulo = ?, autor = ?, disponible = ?, isbn = ? WHERE id = ?",
                (titulo, autor, val_disponible, isbn, id_libro)
            )
            conexion.commit()
        finally:
            conexion.close()

    @staticmethod
    def borrar_de_bd(id_libro):
        """Elimina permanentemente la fila de un libro usando su ID"""
        conexion = sqlite3.connect(RUTA_BD, timeout=10.0)
        try:
            conexion.execute("DELETE FROM libros WHERE id = ?", (id_libro,))
            conexion.commit()
        finally:
            conexion.close()