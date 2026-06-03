import unittest
from unittest.mock import patch, MagicMock, call
from datetime import date
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from DTO.Prestamo import Prestamo
from DAO.PrestamoDAO import PrestamoDAO


# ===========================================================================
# TESTS DE Prestamo.py
# ===========================================================================

class TestPrestamoInit(unittest.TestCase):
    """Cubre __init__: con todos los atributos y con valores por defecto."""

    def test_crea_prestamo_con_todos_los_atributos(self):
        prestamo = Prestamo(1, 10, 5, date(2025, 1, 1), date(2025, 1, 31))
        self.assertEqual(prestamo.id_prestamo, 1)
        self.assertEqual(prestamo.libro_id, 10)
        self.assertEqual(prestamo.usuario_id, 5)
        self.assertEqual(prestamo.fecha_prestamo, date(2025, 1, 1))
        self.assertEqual(prestamo.fecha_devolucion, date(2025, 1, 31))

    def test_fechas_por_defecto_son_none(self):
        prestamo = Prestamo(2, 3, 4)
        self.assertIsNone(prestamo.fecha_prestamo)
        self.assertIsNone(prestamo.fecha_devolucion)

    def test_estado_no_se_guarda_como_atributo(self):
        # El parámetro 'estado' existe en la firma pero no se asigna en __init__
        prestamo = Prestamo(1, 1, 1, estado="devuelto")
        self.assertFalse(hasattr(prestamo, "estado"))


class TestPrestamoStr(unittest.TestCase):
    """Cubre __str__: formato completo con fechas y sin ellas."""

    def test_str_con_fechas(self):
        prestamo = Prestamo(1, 10, 5, date(2025, 3, 1), date(2025, 3, 31))
        esperado = (
            "Prestamo 1 | "
            "Libro: 10 | "
            "Usuario: 5 | "
            f"Desde: {date(2025, 3, 1)} | "
            f"Hasta: {date(2025, 3, 31)}"
        )
        self.assertEqual(str(prestamo), esperado)

    def test_str_con_fechas_none(self):
        prestamo = Prestamo(2, 7, 3)
        esperado = (
            "Prestamo 2 | "
            "Libro: 7 | "
            "Usuario: 3 | "
            "Desde: None | "
            "Hasta: None"
        )
        self.assertEqual(str(prestamo), esperado)


# ===========================================================================
# TESTS DE PrestamoDAO.py
# ===========================================================================

def _mock_conexion():
    """Helper: devuelve un mock de conexión SQLite listo para usar con 'with'."""
    mock_conn = MagicMock()
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    return mock_conn


class TestRegistrarPrestamo(unittest.TestCase):
    """Cubre registrar_prestamo: inserción exitosa y retorno del ID generado."""

    def test_inserta_y_devuelve_id(self):
        mock_conn = _mock_conexion()
        mock_cursor = MagicMock()
        mock_cursor.lastrowid = 42
        mock_conn.cursor.return_value = mock_cursor

        with patch("DAO.PrestamoDAO.sqlite3.connect", return_value=mock_conn):
            dao = PrestamoDAO()
            id_generado = dao.registrar_prestamo(1, 2, date(2025, 1, 1), date(2025, 1, 31))

        self.assertEqual(id_generado, 42)
        mock_cursor.execute.assert_called_once()
        args = mock_cursor.execute.call_args[0]
        self.assertIn("INSERT INTO prestamos", args[0])
        self.assertEqual(args[1], (1, 2, date(2025, 1, 1), date(2025, 1, 31)))
        mock_conn.commit.assert_called_once()

    def test_hace_commit_correctamente(self):
        mock_conn = _mock_conexion()
        mock_cursor = MagicMock()
        mock_cursor.lastrowid = 99
        mock_conn.cursor.return_value = mock_cursor

        with patch("DAO.PrestamoDAO.sqlite3.connect", return_value=mock_conn):
            PrestamoDAO().registrar_prestamo(5, 3, date(2025, 2, 1), date(2025, 2, 28))

        mock_conn.commit.assert_called_once()


class TestTienePrestamoActivo(unittest.TestCase):
    """Cubre tiene_prestamo_activo: con fila encontrada y sin fila."""

    def test_devuelve_true_cuando_hay_prestamo(self):
        mock_conn = _mock_conexion()
        mock_conn.execute.return_value.fetchone.return_value = (1,)

        with patch("DAO.PrestamoDAO.sqlite3.connect", return_value=mock_conn):
            resultado = PrestamoDAO().tiene_prestamo_activo(10)

        self.assertTrue(resultado)

    def test_devuelve_false_cuando_no_hay_prestamo(self):
        mock_conn = _mock_conexion()
        mock_conn.execute.return_value.fetchone.return_value = None

        with patch("DAO.PrestamoDAO.sqlite3.connect", return_value=mock_conn):
            resultado = PrestamoDAO().tiene_prestamo_activo(10)

        self.assertFalse(resultado)


class TestGetPrestamoActivo(unittest.TestCase):
    """Cubre get_prestamo_activo: fila encontrada y fila no encontrada."""

    def test_devuelve_objeto_prestamo_cuando_existe(self):
        fila = (1, 10, 5, date(2025, 1, 1), date(2025, 1, 31))
        mock_conn = _mock_conexion()
        mock_conn.execute.return_value.fetchone.return_value = fila

        with patch("DAO.PrestamoDAO.sqlite3.connect", return_value=mock_conn):
            prestamo = PrestamoDAO().get_prestamo_activo(10)

        self.assertIsNotNone(prestamo)
        self.assertIsInstance(prestamo, Prestamo)
        self.assertEqual(prestamo.id_prestamo, 1)
        self.assertEqual(prestamo.libro_id, 10)
        self.assertEqual(prestamo.usuario_id, 5)
        self.assertEqual(prestamo.fecha_prestamo, date(2025, 1, 1))
        self.assertEqual(prestamo.fecha_devolucion, date(2025, 1, 31))

    def test_devuelve_none_cuando_no_existe(self):
        mock_conn = _mock_conexion()
        mock_conn.execute.return_value.fetchone.return_value = None

        with patch("DAO.PrestamoDAO.sqlite3.connect", return_value=mock_conn):
            resultado = PrestamoDAO().get_prestamo_activo(99)

        self.assertIsNone(resultado)


class TestDevolverPrestamo(unittest.TestCase):
    """Cubre devolver_prestamo: DELETE ejecutado y commit realizado."""

    def test_ejecuta_delete_y_hace_commit(self):
        mock_conn = _mock_conexion()

        with patch("DAO.PrestamoDAO.sqlite3.connect", return_value=mock_conn):
            PrestamoDAO().devolver_prestamo(5)

        mock_conn.execute.assert_called_once()
        sql = mock_conn.execute.call_args[0][0]
        self.assertIn("DELETE FROM prestamos", sql)
        params = mock_conn.execute.call_args[0][1]
        self.assertEqual(params, (5,))
        mock_conn.commit.assert_called_once()


class TestListarPrestamosUsuario(unittest.TestCase):
    """Cubre listar_prestamos_usuario: lista con resultados, lista vacía."""

    def test_devuelve_lista_de_objetos_prestamo(self):
        filas = [
            (1, 10, 5, date(2025, 1, 1), date(2025, 1, 31)),
            (2, 11, 5, date(2025, 2, 1), date(2025, 2, 28)),
        ]
        mock_conn = _mock_conexion()
        mock_conn.execute.return_value.fetchall.return_value = filas

        with patch("DAO.PrestamoDAO.sqlite3.connect", return_value=mock_conn):
            resultado = PrestamoDAO().listar_prestamos_usuario(5)

        self.assertEqual(len(resultado), 2)
        self.assertIsInstance(resultado[0], Prestamo)
        self.assertEqual(resultado[0].id_prestamo, 1)
        self.assertEqual(resultado[0].libro_id, 10)
        self.assertIsInstance(resultado[1], Prestamo)
        self.assertEqual(resultado[1].id_prestamo, 2)

    def test_devuelve_lista_vacia_sin_prestamos(self):
        mock_conn = _mock_conexion()
        mock_conn.execute.return_value.fetchall.return_value = []

        with patch("DAO.PrestamoDAO.sqlite3.connect", return_value=mock_conn):
            resultado = PrestamoDAO().listar_prestamos_usuario(99)

        self.assertEqual(resultado, [])

    def test_consulta_filtra_por_usuario_id(self):
        mock_conn = _mock_conexion()
        mock_conn.execute.return_value.fetchall.return_value = []

        with patch("DAO.PrestamoDAO.sqlite3.connect", return_value=mock_conn):
            PrestamoDAO().listar_prestamos_usuario(7)

        params = mock_conn.execute.call_args[0][1]
        self.assertEqual(params, (7,))


if __name__ == "__main__":
    unittest.main(verbosity=2)