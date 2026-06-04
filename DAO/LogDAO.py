import sqlite3
from pathlib import Path
from DTO.Log import Log

RUTA_BD = Path(__file__).resolve().parent.parent / "bd" / "biblioteca.db"


class LogDAO:
    def insertar_log(self,usuario_id,usuario_nombre,accion,libro_id,libro_titulo):
        with sqlite3.connect(RUTA_BD) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO log (usuario_id,usuario_nombre,accion,libro_id,libro_titulo) VALUES (?, ?, ?, ?, ?)
                """,
                (usuario_id,usuario_nombre,accion,libro_id,libro_titulo)
            )

            conn.commit()
            return cursor.lastrowid

    def obtener_logs_por_usuario(self, usuario_id):
        with sqlite3.connect(RUTA_BD) as conn:
            filas = conn.execute(
                """
                SELECT id_log,usuario_id,usuario_nombre,accion,libro_id,libro_titulo FROM log WHERE usuario_id = ? ORDER BY id_log DESC
                """,
                (usuario_id,)
            ).fetchall()

        return [
            Log(f[0], f[1], f[2], f[3], f[4], f[5])
            for f in filas
        ]

    def obtener_logs_por_libro(self, libro_id):
        with sqlite3.connect(RUTA_BD) as conn:
            filas = conn.execute(
                """
                SELECT id_log, usuario_id,usuario_nombre,accion,libro_id,libro_titulo FROM log WHERE libro_id = ? ORDER BY id_log DESC
                """,
                (libro_id,)
            ).fetchall()

        return [
            Log(f[0], f[1], f[2], f[3], f[4], f[5])
            for f in filas
        ]