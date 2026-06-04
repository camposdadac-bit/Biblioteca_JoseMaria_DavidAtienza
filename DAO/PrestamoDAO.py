import sqlite3
from pathlib import Path
from DTO.Prestamo import Prestamo

RUTA_BD = Path(__file__).resolve().parent.parent / "bd" / "biblioteca.db"


class PrestamoDAO:

    def registrar_prestamo(self,libro_id,usuario_id,fecha_prestamo,fecha_devolucion):
        with sqlite3.connect(RUTA_BD) as conexion:
            cursor = conexion.cursor()

            cursor.execute(
                """INSERT INTO prestamos (libro_id, usuario_id, fecha_prestamo, fecha_devolucion) VALUES (?, ?, ?, ?)""",
                (libro_id,usuario_id,fecha_prestamo,fecha_devolucion)
            )

            conexion.commit()
            return cursor.lastrowid

    def tiene_prestamo_activo(self, libro_id):
        with sqlite3.connect(RUTA_BD) as conexion:
            fila = conexion.execute(
                """SELECT 1 FROM prestamos WHERE libro_id = ? LIMIT 1""",
                (libro_id,)
            ).fetchone()

        return fila is not None

    def devolver_prestamo(self, libro_id):
        with sqlite3.connect(RUTA_BD) as conexion:
            conexion.execute(
                """DELETE FROM prestamos WHERE libro_id = ?""",
                (libro_id,)
            )

            conexion.commit()

    def listar_prestamos_usuario(self, usuario_id):
        with sqlite3.connect(RUTA_BD) as conexion:
            filas = conexion.execute(
                """SELECT id_prestamo,libro_id,usuario_id,fecha_prestamo,fecha_devolucion FROM prestamos WHERE usuario_id = ? ORDER BY fecha_prestamo""",
                (usuario_id,)
            ).fetchall()

        prestamos = []

        for fila in filas:
            prestamos.append(
                Prestamo(fila[0],fila[1],fila[2],fila[3],fila[4])
            )

        return prestamos