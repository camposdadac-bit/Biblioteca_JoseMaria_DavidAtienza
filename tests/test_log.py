import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from DTO.Log import Log
from DAO.LogDAO import LogDAO


# ===========================================================================
# TESTS DE Log.py
# ===========================================================================

class TestLog(unittest.TestCase):
    """Cubre __init__ y __str__ de Log."""

    def setUp(self):
        self.log = Log(1, 10, "Ana", "ha pedido prestado el libro", 5, "1984")

    def test_atributos(self):
        """Comprueba que __init__ guarda correctamente todos los atributos."""
        self.assertEqual(self.log.id_log, 1)
        self.assertEqual(self.log.id_usuario, 10)
        self.assertEqual(self.log.usuario_nombre, "Ana")
        self.assertEqual(self.log.accion, "ha pedido prestado el libro")
        self.assertEqual(self.log.id_libro, 5)
        self.assertEqual(self.log.libro_titulo, "1984")

    def test_str(self):
        """Comprueba que __str__ devuelve el formato correcto."""
        esperado = "Usuario: Ana | Acción: ha pedido prestado el libro | Libro: 1984"
        self.assertEqual(str(self.log), esperado)


# ===========================================================================
# TESTS DE LogDAO.py
# ===========================================================================

def _mock_conn():
    """Crea una conexión falsa que funciona con el bloque 'with'."""
    mock = MagicMock()
    mock.__enter__ = MagicMock(return_value=mock)
    mock.__exit__ = MagicMock(return_value=False)
    return mock


class TestLogDAO(unittest.TestCase):
    """Cubre los tres métodos de LogDAO: insertar, obtener por usuario, obtener por libro."""

    def test_insertar_log_devuelve_id(self):
        """Comprueba que el INSERT se ejecuta, hace commit y devuelve el ID generado."""
        conn = _mock_conn()
        conn.cursor.return_value.lastrowid = 7
        with patch("DAO.LogDAO.sqlite3.connect", return_value=conn):
            resultado = LogDAO().insertar_log(1, "Ana", "prestó", 5, "1984")
        self.assertEqual(resultado, 7)
        conn.commit.assert_called_once()

    def test_obtener_logs_por_usuario_devuelve_lista(self):
        """Comprueba que devuelve una lista de objetos Log cuando hay filas."""
        filas = [(1, 10, "Ana", "prestó", 5, "1984")]
        conn = _mock_conn()
        conn.execute.return_value.fetchall.return_value = filas
        with patch("DAO.LogDAO.sqlite3.connect", return_value=conn):
            resultado = LogDAO().obtener_logs_por_usuario(10)
        self.assertEqual(len(resultado), 1)
        self.assertIsInstance(resultado[0], Log)

    def test_obtener_logs_por_usuario_vacio(self):
        """Comprueba que devuelve lista vacía cuando no hay logs del usuario."""
        conn = _mock_conn()
        conn.execute.return_value.fetchall.return_value = []
        with patch("DAO.LogDAO.sqlite3.connect", return_value=conn):
            resultado = LogDAO().obtener_logs_por_usuario(99)
        self.assertEqual(resultado, [])

    def test_obtener_logs_por_libro_devuelve_lista(self):
        """Comprueba que devuelve una lista de objetos Log cuando hay filas."""
        filas = [(1, 10, "Ana", "prestó", 5, "1984")]
        conn = _mock_conn()
        conn.execute.return_value.fetchall.return_value = filas
        with patch("DAO.LogDAO.sqlite3.connect", return_value=conn):
            resultado = LogDAO().obtener_logs_por_libro(5)
        self.assertEqual(len(resultado), 1)
        self.assertIsInstance(resultado[0], Log)

    def test_obtener_logs_por_libro_vacio(self):
        """Comprueba que devuelve lista vacía cuando no hay logs del libro."""
        conn = _mock_conn()
        conn.execute.return_value.fetchall.return_value = []
        with patch("DAO.LogDAO.sqlite3.connect", return_value=conn):
            resultado = LogDAO().obtener_logs_por_libro(99)
        self.assertEqual(resultado, [])


if __name__ == "__main__":
    unittest.main()