import sqlite3
from pathlib import Path
from DTO.Usuario import Usuario

RUTA_BD = Path(__file__).resolve().parent.parent / "bd" / "biblioteca.db"

class UsuarioDAO:
    def add_usuario_bd(self, usuario):
        """Inserta en la tabla usuarios los datos que le hemos pasado, convirtiendo habilitado a 1 o 0, y devuelve el ID generado."""
        val_habilitado = 1 if usuario.habilitado else 0

        with sqlite3.connect(RUTA_BD) as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nombre, apellidos, email, habilitado) VALUES (?, ?, ?, ?)",
                (usuario.nombre, usuario.apellidos, usuario.email, val_habilitado)
            )
            conexion.commit()
            return cursor.lastrowid


    def get_usuario_id_bd(self, id_usuario):
        """Busca un usuario por ID, si existe devuelve un objeto Usuario convirtiendo el 0/1 de la BD a bool, si no existe devuelve None"""
        with sqlite3.connect(RUTA_BD) as conexion:
            fila = conexion.execute(
                "SELECT id, nombre, apellidos, email, habilitado FROM usuarios WHERE id = ?",
                (id_usuario,)
            ).fetchone()

        if fila:
            return Usuario(fila[0], fila[1], fila[2], fila[3], bool(fila[4]))

        return None


    def seleccionar_todos(self):
        """Trae todas las filas de la tabla y las convierte en objetos Usuario"""
        with sqlite3.connect(RUTA_BD) as conexion:
            filas = conexion.execute(
                "SELECT id, nombre, apellidos, email, habilitado FROM usuarios"
            ).fetchall()

        lista = []

        for fila in filas:
            lista.append(
                Usuario(fila[0], fila[1], fila[2], fila[3], bool(fila[4]))
            )

        return lista

    def update_usuario_bd(self, id_usuario, nombre, apellidos, email, habilitado):
        """Convierte habilitado a 1 o 0 y ejecuta el UPDATE con todos los campos filtrando por ID"""
        val_habilitado = 1 if habilitado else 0

        with sqlite3.connect(RUTA_BD) as conexion:
            conexion.execute(
                """UPDATE usuarios SET nombre = ?, apellidos = ?, email = ?, habilitado = ? WHERE id = ?""",
                (nombre, apellidos, email, val_habilitado, id_usuario)
            )
            conexion.commit()

    def borrar_de_bd(self, id_usuario):
        """Ejecuta un DELETE filtrando por ID"""
        with sqlite3.connect(RUTA_BD) as conexion:
            conexion.execute(
                "DELETE FROM usuarios WHERE id = ?",
                (id_usuario,)
            )
            conexion.commit()

    def buscar_por_nombre_bd(self, nombre):
        """Busca usuarios cuyo nombre coincida ignorando mayúsculas"""
        with sqlite3.connect(RUTA_BD) as conexion:
            filas = conexion.execute(
                """SELECT id, nombre, apellidos, email, habilitado FROM usuarios WHERE LOWER(nombre) = LOWER(?)""",
                (nombre,)
            ).fetchall()

        return [
            Usuario(f[0], f[1], f[2], f[3], bool(f[4]))
            for f in filas
        ]

    def buscar_por_apellidos_bd(self, apellidos):
        """Igual que buscar_por_nombre_bd pero filtrando por apellidos ignorando mayúsculas"""
        with sqlite3.connect(RUTA_BD) as conexion:
            filas = conexion.execute(
                """SELECT id, nombre, apellidos, email, habilitado FROM usuarios WHERE LOWER(apellidos) = LOWER(?)""",
                (apellidos,)
            ).fetchall()

        return [
            Usuario(f[0], f[1], f[2], f[3], bool(f[4]))
            for f in filas
        ]

    def buscar_por_email_bd(self, email):
        """Busca un único usuario por email ignorando mayúsculas"""
        with sqlite3.connect(RUTA_BD) as conexion:
            fila = conexion.execute(
                """SELECT id, nombre, apellidos, email, habilitado FROM usuarios WHERE LOWER(email) = LOWER(?)""",
                (email,)
            ).fetchone()

        if fila is None:
            return None

        return Usuario(fila[0], fila[1], fila[2], fila[3], bool(fila[4]))