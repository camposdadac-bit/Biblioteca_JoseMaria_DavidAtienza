import unittest
from unittest.mock import patch, MagicMock
import sqlite3
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from DTO.Libro import Libro
from DAO.DAO_libro import DAO_libro

class test_libro(unittest.TestCase):
    """Cubre __init__: con y sin valores opcionales."""

    def test_crea_libro_con_todos_los_atributos(self):
        libro = Libro(1, "Titulo", "Autor", disponible=False, isbn="978-0")
        self.assertEqual(libro.id, 1)
        self.assertEqual(libro.titulo, "Titulo")
        self.assertEqual(libro.autor, "Autor")
        self.assertFalse(libro.disponible)
        self.assertEqual(libro.isbn, "978-0")

    def test_disponible_por_defecto_es_true(self):
        libro = Libro(2, "T", "A")
        self.assertTrue(libro.disponible)

    def test_isbn_por_defecto_es_none(self):
        libro = Libro(3, "T", "A")
        self.assertIsNone(libro.isbn)


class TestLibroStr(unittest.TestCase):
    """Cubre __str__: libro disponible y libro prestado."""

    def test_str_libro_disponible(self):
        libro = Libro(1, "Quijote", "Cervantes", disponible=True)
        self.assertEqual(str(libro), "Quijote - Cervantes - Disponible")

    def test_str_libro_prestado(self):
        libro = Libro(2, "1984", "Orwell", disponible=False)
        self.assertEqual(str(libro), "1984 - Orwell - Prestado")


def _make_mock_conexion(fetchone=None, fetchall=None):
    """Helper: devuelve un mock de conexión SQLite configurado."""
    mock_cursor = MagicMock()
    mock_cursor.lastrowid = 99

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.execute.return_value.fetchone.return_value = fetchone
    mock_conn.execute.return_value.fetchall.return_value = fetchall or []

    return mock_conn, mock_cursor


class TestDAOInsertar(unittest.TestCase):
    """Cubre insertar_en_bd: inserción exitosa con disponible True y False."""

    def test_inserta_libro_disponible_y_devuelve_id(self):
        mock_conn, mock_cursor = _make_mock_conexion()
        with patch("DAO.DAO_libro.sqlite3.connect", return_value=mock_conn):
            id_generado = DAO_libro.insertar_en_bd("Titulo", "Autor", True, "isbn1")
        self.assertEqual(id_generado, 99)
        mock_cursor.execute.assert_called_once()
        # Verifica que disponible se convierte a 1
        args = mock_cursor.execute.call_args[0]
        self.assertIn(1, args[1])

    def test_inserta_libro_no_disponible_pasa_cero(self):
        mock_conn, mock_cursor = _make_mock_conexion()
        with patch("DAO.DAO_libro.sqlite3.connect", return_value=mock_conn):
            DAO_libro.insertar_en_bd("Titulo", "Autor", False, "isbn2")
        args = mock_cursor.execute.call_args[0]
        self.assertIn(0, args[1])

    def test_cierra_conexion_aunque_falle(self):
        mock_conn, mock_cursor = _make_mock_conexion()
        mock_cursor.execute.side_effect = sqlite3.OperationalError("fallo")
        with patch("DAO.DAO_libro.sqlite3.connect", return_value=mock_conn):
            with self.assertRaises(sqlite3.OperationalError):
                DAO_libro.insertar_en_bd("T", "A", True, "i")
        mock_conn.close.assert_called_once()


class TestDAOSeleccionarPorId(unittest.TestCase):
    """Cubre seleccionar_por_id: fila encontrada y fila no encontrada."""

    def test_devuelve_objeto_libro_cuando_existe(self):
        fila = (1, "Don Quijote", "Cervantes", 1, "978-1")
        mock_conn, _ = _make_mock_conexion(fetchone=fila)
        with patch("DAO.DAO_libro.sqlite3.connect", return_value=mock_conn):
            libro = DAO_libro.seleccionar_por_id(1)
        self.assertIsNotNone(libro)
        self.assertIsInstance(libro, Libro)
        self.assertEqual(libro.id, 1)
        self.assertEqual(libro.titulo, "Don Quijote")
        self.assertTrue(libro.disponible)  # 1 → True

    def test_disponible_false_cuando_bd_tiene_cero(self):
        fila = (2, "Titulo", "Autor", 0, "isbn")
        mock_conn, _ = _make_mock_conexion(fetchone=fila)
        with patch("DAO.DAO_libro.sqlite3.connect", return_value=mock_conn):
            libro = DAO_libro.seleccionar_por_id(2)
        self.assertFalse(libro.disponible)

    def test_devuelve_none_cuando_no_existe(self):
        mock_conn, _ = _make_mock_conexion(fetchone=None)
        with patch("DAO.DAO_libro.sqlite3.connect", return_value=mock_conn):
            resultado = DAO_libro.seleccionar_por_id(999)
        self.assertIsNone(resultado)

    def test_cierra_conexion_aunque_falle(self):
        mock_conn = MagicMock()
        mock_conn.execute.side_effect = sqlite3.OperationalError("error")
        with patch("DAO.DAO_libro.sqlite3.connect", return_value=mock_conn):
            with self.assertRaises(sqlite3.OperationalError):
                DAO_libro.seleccionar_por_id(1)
        mock_conn.close.assert_called_once()


class TestDAOSeleccionarTodos(unittest.TestCase):
    """Cubre seleccionar_todos: lista con elementos y lista vacía."""

    def test_devuelve_lista_de_objetos_libro(self):
        filas = [
            (1, "Libro1", "Autor1", 1, "isbn1"),
            (2, "Libro2", "Autor2", 0, "isbn2"),
        ]
        mock_conn, _ = _make_mock_conexion(fetchall=filas)
        with patch("DAO.DAO_libro.sqlite3.connect", return_value=mock_conn):
            resultado = DAO_libro.seleccionar_todos()
        self.assertEqual(len(resultado), 2)
        self.assertIsInstance(resultado[0], Libro)
        self.assertTrue(resultado[0].disponible)
        self.assertFalse(resultado[1].disponible)

    def test_devuelve_lista_vacia_si_no_hay_filas(self):
        mock_conn, _ = _make_mock_conexion(fetchall=[])
        with patch("DAO.DAO_libro.sqlite3.connect", return_value=mock_conn):
            resultado = DAO_libro.seleccionar_todos()
        self.assertEqual(resultado, [])

    def test_cierra_conexion_aunque_falle(self):
        mock_conn = MagicMock()
        mock_conn.execute.side_effect = sqlite3.OperationalError("error")
        with patch("DAO.DAO_libro.sqlite3.connect", return_value=mock_conn):
            with self.assertRaises(sqlite3.OperationalError):
                DAO_libro.seleccionar_todos()
        mock_conn.close.assert_called_once()


class TestDAOModificar(unittest.TestCase):
    """Cubre modificar_en_bd: actualización con disponible True y False."""

    def test_modifica_libro_disponible(self):
        mock_conn = MagicMock()
        with patch("DAO.DAO_libro.sqlite3.connect", return_value=mock_conn):
            DAO_libro.modificar_en_bd(1, "Nuevo Titulo", "Nuevo Autor", True, "isbn_new")
        mock_conn.execute.assert_called_once()
        args = mock_conn.execute.call_args[0]
        self.assertIn(1, args[1])  # disponible = 1

    def test_modifica_libro_no_disponible(self):
        mock_conn = MagicMock()
        with patch("DAO.DAO_libro.sqlite3.connect", return_value=mock_conn):
            DAO_libro.modificar_en_bd(1, "Titulo", "Autor", False, "isbn")
        args = mock_conn.execute.call_args[0]
        self.assertIn(0, args[1])  # disponible = 0

    def test_hace_commit_y_cierra_conexion(self):
        mock_conn = MagicMock()
        with patch("DAO.DAO_libro.sqlite3.connect", return_value=mock_conn):
            DAO_libro.modificar_en_bd(1, "T", "A", True, "i")
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    def test_cierra_conexion_aunque_falle(self):
        mock_conn = MagicMock()
        mock_conn.execute.side_effect = sqlite3.OperationalError("error")
        with patch("DAO.DAO_libro.sqlite3.connect", return_value=mock_conn):
            with self.assertRaises(sqlite3.OperationalError):
                DAO_libro.modificar_en_bd(1, "T", "A", True, "i")
        mock_conn.close.assert_called_once()


class TestDAOBorrar(unittest.TestCase):
    """Cubre borrar_de_bd: borrado exitoso y cierre de conexión en fallo."""

    def test_ejecuta_delete_y_hace_commit(self):
        mock_conn = MagicMock()
        with patch("DAO.DAO_libro.sqlite3.connect", return_value=mock_conn):
            DAO_libro.borrar_de_bd(5)
        mock_conn.execute.assert_called_once()
        sql = mock_conn.execute.call_args[0][0]
        self.assertIn("DELETE", sql)
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    def test_cierra_conexion_aunque_falle(self):
        mock_conn = MagicMock()
        mock_conn.execute.side_effect = sqlite3.OperationalError("error")
        with patch("DAO.DAO_libro.sqlite3.connect", return_value=mock_conn):
            with self.assertRaises(sqlite3.OperationalError):
                DAO_libro.borrar_de_bd(5)
        mock_conn.close.assert_called_once()


if __name__ == "__main__":
    unittest.main(verbosity=2)