import sqlite3
import unittest
from pathlib import Path
import warnings
RUTA_BD = Path(__file__).resolve().parent.parent / "bd" / "biblioteca.db"

class TestBaseDatosInicial(unittest.TestCase):
    def test_biblioteca_db_estructura_correcta(self):
        self.assertTrue(RUTA_BD.exists(), "La base de datos no existe en la ruta definida")
        warnings.filterwarnings("ignore", category=ResourceWarning)
        with sqlite3.connect(RUTA_BD) as conexion:
            """Validar tabla libros'"""
            tablas_libros = conexion.execute("PRAGMA table_info(libros)").fetchall()
            columnas_libros = [info[1] for info in tablas_libros]
            columnas_esperadas_libros = ["id", "titulo", "autor", "isbn", "disponible", "categoria", "fecha_actualizacion"]
            self.assertEqual(columnas_libros, columnas_esperadas_libros, "Error en estructura de tabla 'libros'")

            """Validar tabla usuarios"""
            tablas_usuarios = conexion.execute("PRAGMA table_info(usuarios)").fetchall()
            columnas_usuarios = [info[1] for info in tablas_usuarios]
            columnas_esperadas_usuarios = ["id_usuario", "nombre", "apellidos", "email", "habilitado"]
            self.assertEqual(columnas_usuarios, columnas_esperadas_usuarios, "Error en estructura de tabla 'usuarios'")

        conexion.close()

if __name__ == "__main__":
    unittest.main()