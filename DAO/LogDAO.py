import sqlite3
from pathlib import Path
from DTO.Log import Log

RUTA_BD = Path(__file__).resolve().parent.parent / "bd" / "biblioteca.db"


class LogDAO:
    def insertar_log(self,usuario_id,usuario_nombre,accion,libro_id,libro_titulo):
        """Insertar los logs en la base de datos"""
        with sqlite3.connect(RUTA_BD) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO log (usuario_id,usuario_nombre,accion,libro_id,libro_titulo) VALUES (?, ?, ?, ?, ?)""",
                (usuario_id,usuario_nombre,accion,libro_id,libro_titulo)
            )

            conn.commit()
            return cursor.lastrowid

    def obtener_logs_por_usuario(self, usuario_id):
        """Obtiene el log del usuario que tu le hayas dicho"""
        with sqlite3.connect(RUTA_BD) as conn:
            filas = conn.execute(
                """SELECT id_log,usuario_id,usuario_nombre,accion,libro_id,libro_titulo FROM log WHERE usuario_id = ? ORDER BY id_log DESC""",
                (usuario_id,)
            ).fetchall()

        return [
            Log(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5])
            for fila in filas
        ]

    def obtener_logs_por_libro(self, libro_id):
        """Obtiene el log del log que tu le hayas dicho"""
        with sqlite3.connect(RUTA_BD) as conn:
            filas = conn.execute(
                """SELECT id_log, usuario_id,usuario_nombre,accion,libro_id,libro_titulo FROM log WHERE libro_id = ? ORDER BY id_log DESC""",
                (libro_id,)
            ).fetchall()

        return [
            Log(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5])
            for fila in filas
        ]