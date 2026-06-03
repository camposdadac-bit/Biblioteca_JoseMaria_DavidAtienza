import sqlite3
from pathlib import Path
from DTO.Prestamo import Prestamo

RUTA_BD = Path(__file__).resolve().parent.parent / "bd" / "biblioteca.db"


class PrestamoDAO:
    def registrar_prestamo(self, libro_id, usuario_id):
        with sqlite3.connect(RUTA_BD) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO prestamos (libro_id, usuario_id, estado)
                VALUES (?, ?, 'prestado')
                """,
                (libro_id, usuario_id)
            )

            conn.commit()
            return cursor.lastrowid

    def get_prestamo_activo(self, libro_id, usuario_id):
        with sqlite3.connect(RUTA_BD) as conn:
            fila = conn.execute(
                """
                SELECT id_prestamo, libro_id, usuario_id, fecha_prestamo, fecha_devolucion, estado
                FROM prestamos
                WHERE libro_id = ?
                  AND usuario_id = ?
                  AND estado = 'prestado'
                """,
                (libro_id, usuario_id)
            ).fetchone()

        if fila is None:
            return None

        return Prestamo(fila[0],fila[1],fila[2],fila[3],fila[4],fila[5])

    def registrar_devolucion(self, id_prestamo):
        with sqlite3.connect(RUTA_BD) as conexion:
            conexion.execute(
                """
                UPDATE prestamos
                SET estado = 'devuelto',
                    fecha_devolucion = DATE('now')
                WHERE id_prestamo = ?
                  AND estado = 'prestado'
                """,
                (id_prestamo,)
            )

            conexion.commit()