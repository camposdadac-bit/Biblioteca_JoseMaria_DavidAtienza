import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Añadimos la raíz del proyecto al path para que los imports funcionen
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import biblioteca
from DTO.Libro import Libro
from DTO.Usuario import Usuario

class TestBibliotecaBase(unittest.TestCase):
    def setUp(self):
        """Restaura el estado global de biblioteca antes de cada test."""
        biblioteca.bd = []
        biblioteca.libros = []
        biblioteca.usuarios = []
        biblioteca.modo = "normal"
        biblioteca.ultimo_error = ""

    def tearDown(self):
        """Restaura el estado global de biblioteca después de cada test."""
        biblioteca.bd = []
        biblioteca.libros = []
        biblioteca.usuarios = []
        biblioteca.modo = "normal"
        biblioteca.ultimo_error = ""


def _reset_biblioteca():
    """Reinicia el estado global de biblioteca entre tests."""
    biblioteca.libros.clear()
    biblioteca.bd = biblioteca.libros
    biblioteca.modo = "normal"
    biblioteca.ultimo_error = ""
    biblioteca.proximo_id = 1


class TestMostrarMensaje(unittest.TestCase):
    """Cubre los tres tipos (0, 1, 2) de mostrar_mensaje."""

    def test_tipo_1_imprime_mensaje_y_titulo(self):
        with patch("builtins.print") as mock_print:
            biblioteca.mostrar_mensaje("Hola ", "Mundo", tipo=1)
            mock_print.assert_called_once_with("Hola Mundo")

    def test_tipo_2_imprime_solo_mensaje(self):
        with patch("builtins.print") as mock_print:
            biblioteca.mostrar_mensaje("Solo mensaje", tipo=2)
            mock_print.assert_called_once_with("Solo mensaje")

    def test_tipo_0_imprime_str_del_argumento(self):
        with patch("builtins.print") as mock_print:
            biblioteca.mostrar_mensaje(42)
            mock_print.assert_called_once_with("42")


class TestCambiarEstadoLibro(unittest.TestCase):
    """Cubre las tres ramas de cambiar_estado_libro."""

    def setUp(self):
        self.libro = Libro(1, "Titulo", "Autor", disponible=True)

    def test_prestar_libro_cambia_disponible_a_false(self):
        with patch("builtins.print"):
            resultado = biblioteca.cambiar_estado_libro("prestar", self.libro)
        self.assertFalse(self.libro.disponible)
        self.assertEqual(resultado, "Libro prestado")

    def test_devolver_libro_cambia_disponible_a_true(self):
        self.libro.disponible = False
        with patch("builtins.print"):
            resultado = biblioteca.cambiar_estado_libro("devolver", self.libro)
        self.assertTrue(self.libro.disponible)
        self.assertEqual(resultado, "Libro devuelto")

    def test_accion_desconocida_devuelve_mensaje_error(self):
        resultado = biblioteca.cambiar_estado_libro("volar", self.libro)
        self.assertEqual(resultado, "Accion no reconocida")


class TestCrearLibro(unittest.TestCase):
    """Cubre crear_libro y el incremento de proximo_id."""

    def setUp(self):
        _reset_biblioteca()

    def test_crea_libro_con_atributos_correctos(self):
        libro = biblioteca.crear_libro("Don Quijote", "Cervantes", isbn="111")
        self.assertEqual(libro.titulo, "Don Quijote")
        self.assertEqual(libro.autor, "Cervantes")
        self.assertEqual(libro.isbn, "111")
        self.assertTrue(libro.disponible)
        self.assertEqual(libro.id, 1)

    def test_incrementa_proximo_id_en_cada_llamada(self):
        biblioteca.crear_libro("Libro A", "Autor A")
        biblioteca.crear_libro("Libro B", "Autor B")
        self.assertEqual(biblioteca.proximo_id, 3)

    def test_isbn_por_defecto_es_none(self):
        libro = biblioteca.crear_libro("Titulo", "Autor")
        self.assertIsNone(libro.isbn)


class TestAgregarLibro(unittest.TestCase):
    """Cubre agregar_libro: modo normal, modo desconocido."""

    def setUp(self):
        _reset_biblioteca()

    def test_agrega_libro_en_modo_normal(self):
        with patch("builtins.print"):
            biblioteca.agregar_libro("Moby Dick", "Melville")
        self.assertEqual(len(biblioteca.bd), 1)
        self.assertEqual(biblioteca.bd[0].titulo, "Moby Dick")
        self.assertEqual(biblioteca.ultimo_error, "")

    def test_modo_distinto_de_normal_no_agrega_y_guarda_error(self):
        biblioteca.modo = "test"
        biblioteca.agregar_libro("Libro Fantasma", "Nadie")
        self.assertEqual(len(biblioteca.bd), 0)
        self.assertEqual(biblioteca.ultimo_error, "modo desconocido")
        biblioteca.modo = "normal"


class TestBuscarLibro(unittest.TestCase):
    """Cubre buscar_libro: encontrado y no encontrado."""

    def setUp(self):
        _reset_biblioteca()
        with patch("builtins.print"):
            biblioteca.agregar_libro("El Principito", "Saint-Exupéry")

    def test_buscar_libro_existente_devuelve_objeto(self):
        libro = biblioteca.buscar_libro("El Principito")
        self.assertIsNotNone(libro)
        self.assertEqual(libro.titulo, "El Principito")

    def test_buscar_libro_inexistente_devuelve_none(self):
        resultado = biblioteca.buscar_libro("Titulo Inventado")
        self.assertIsNone(resultado)


class TestPrestarLibro(unittest.TestCase):
    """Cubre prestar_libro: éxito, no encontrado, no disponible."""

    def setUp(self):
        _reset_biblioteca()
        with patch("builtins.print"):
            biblioteca.agregar_libro("1984", "Orwell")

    def test_prestar_libro_disponible_lo_marca_prestado(self):
        with patch("builtins.print"):
            resultado = biblioteca.prestar_libro("1984",1)
        self.assertEqual(resultado, "Libro prestado")
        self.assertEqual(biblioteca.ultimo_error, "")

    def test_prestar_libro_no_encontrado_devuelve_error(self):
        with patch("builtins.print"):
            resultado = biblioteca.prestar_libro("Inexistente",1)
        self.assertEqual(resultado, "Libro no encontrado")
        self.assertEqual(biblioteca.ultimo_error, "Libro no encontrado")

    def test_prestar_libro_ya_prestado_devuelve_no_disponible(self):
        biblioteca.bd[0].disponible = False
        with patch("builtins.print"):
            resultado = biblioteca.prestar_libro("1984",1)
        self.assertEqual(resultado, "Libro no disponible")
        self.assertEqual(biblioteca.ultimo_error, "Libro no disponible")


class TestDevolverLibro(unittest.TestCase):
    """Cubre devolver_libro: éxito, no encontrado, ya disponible."""

    def setUp(self):
        _reset_biblioteca()
        with patch("builtins.print"):
            biblioteca.agregar_libro("Hamlet", "Shakespeare")
        biblioteca.bd[0].disponible = False  # lo prestamos manualmente

    def test_devolver_libro_prestado_lo_marca_disponible(self):
        with patch("builtins.print"):
            resultado = biblioteca.devolver_libro("Hamlet")
        self.assertEqual(resultado, "Libro devuelto")
        self.assertEqual(biblioteca.ultimo_error, "")

    def test_devolver_libro_no_encontrado_devuelve_error(self):
        with patch("builtins.print"):
            resultado = biblioteca.devolver_libro("Inexistente")
        self.assertEqual(resultado, "Libro no encontrado")
        self.assertEqual(biblioteca.ultimo_error, "Libro no encontrado")

    def test_devolver_libro_ya_disponible_devuelve_error(self):
        biblioteca.bd[0].disponible = True
        with patch("builtins.print"):
            resultado = biblioteca.devolver_libro("Hamlet")
        self.assertEqual(resultado, "Libro ya disponible")
        self.assertEqual(biblioteca.ultimo_error, "Libro ya disponible")


class TestObtenerEstado(unittest.TestCase):
    """Cubre obtener_estado: disponible y prestado."""

    def test_true_devuelve_disponible(self):
        self.assertEqual(biblioteca.obtener_estado(True), "Disponible")

    def test_false_devuelve_prestado(self):
        self.assertEqual(biblioteca.obtener_estado(False), "Prestado")


class TestSimulacionToString(unittest.TestCase):
    """Cubre simulacion_toString con ambos estados de disponibilidad."""

    def test_formato_libro_disponible(self):
        libro = Libro(1, "Titulo", "Autor", disponible=True)
        resultado = biblioteca.simulacion_toString(libro)
        self.assertEqual(resultado, "Titulo - Autor - Disponible")

    def test_formato_libro_prestado(self):
        libro = Libro(2, "Otro", "Escritor", disponible=False)
        resultado = biblioteca.simulacion_toString(libro)
        self.assertEqual(resultado, "Otro - Escritor - Prestado")


class TestMostrarLibros(unittest.TestCase):
    """Cubre mostrar_libros: lista vacía y con elementos."""

    def setUp(self):
        _reset_biblioteca()

    def test_lista_vacia_imprime_no_hay_libros(self):
        with patch("builtins.print") as mock_print:
            biblioteca.mostrar_libros()
            mock_print.assert_called_once_with("No hay libros")

    def test_lista_con_libros_los_imprime(self):
        with patch("builtins.print"):
            biblioteca.agregar_libro("Odisea", "Homero")
        with patch("builtins.print") as mock_print:
            biblioteca.mostrar_libros()
            mock_print.assert_called_once_with("Odisea - Homero - Disponible")


    #=========================
    #TESTING LIBRO
    #=========================
class TestAddLibro(unittest.TestCase):
    """Cubre add_libro: inserción exitosa y fallo con excepción."""

    def setUp(self):
        _reset_biblioteca()

    def test_add_libro_exitoso_devuelve_true_y_actualiza_id(self):
        libro = Libro(None, "Nuevo", "Autor", disponible=True, isbn="999")
        with patch("biblioteca.DAO_libro.insertar_en_bd", return_value=42):
            resultado = biblioteca.add_libro(libro)
        self.assertTrue(resultado)
        self.assertEqual(libro.id, 42)
        self.assertIn(libro, biblioteca.bd)
        self.assertEqual(biblioteca.ultimo_error, "")

    def test_add_libro_con_excepcion_devuelve_false_y_guarda_error(self):
        libro = Libro(None, "Fallido", "Autor")
        with patch("biblioteca.DAO_libro.insertar_en_bd", side_effect=Exception("DB error")):
            resultado = biblioteca.add_libro(libro)
        self.assertFalse(resultado)
        self.assertEqual(biblioteca.ultimo_error, "DB error")


class TestRemoveLibro(unittest.TestCase):
    """Cubre remove_libro: eliminación exitosa y libro no encontrado."""

    def setUp(self):
        _reset_biblioteca()

    def test_remove_libro_existente_devuelve_true_y_lo_elimina_de_bd(self):
        libro = Libro(1, "Para Borrar", "Autor")
        biblioteca.bd.append(libro)
        with patch("biblioteca.DAO_libro.seleccionar_por_id", return_value=libro), \
             patch("biblioteca.DAO_libro.borrar_de_bd") as mock_borrar:
            resultado = biblioteca.remove_libro(1)
        self.assertTrue(resultado)
        mock_borrar.assert_called_once_with(1)
        self.assertNotIn(libro, biblioteca.bd)
        self.assertEqual(biblioteca.ultimo_error, "")

    def test_remove_libro_no_existente_devuelve_false(self):
        with patch("biblioteca.DAO_libro.seleccionar_por_id", return_value=None):
            resultado = biblioteca.remove_libro(99)
        self.assertFalse(resultado)
        self.assertEqual(biblioteca.ultimo_error, "Libro no encontrado")


class TestGetLibro(unittest.TestCase):
    """Cubre get_libro: encontrado y no encontrado."""

    def setUp(self):
        _reset_biblioteca()

    def test_get_libro_existente_devuelve_objeto(self):
        libro = Libro(5, "Existe", "Alguien")
        with patch("biblioteca.DAO_libro.seleccionar_por_id", return_value=libro):
            resultado = biblioteca.get_libro(5)
        self.assertEqual(resultado, libro)
        self.assertEqual(biblioteca.ultimo_error, "")

    def test_get_libro_inexistente_devuelve_none(self):
        with patch("biblioteca.DAO_libro.seleccionar_por_id", return_value=None):
            resultado = biblioteca.get_libro(999)
        self.assertIsNone(resultado)
        self.assertEqual(biblioteca.ultimo_error, "Libro no encontrado")


class TestListLibros(unittest.TestCase):
    """Cubre list_libros: sincronización de bd global con la BD real."""

    def setUp(self):
        _reset_biblioteca()

    def test_list_libros_sincroniza_y_devuelve_lista(self):
        libros_mock = [Libro(1, "A", "X"), Libro(2, "B", "Y")]
        with patch("biblioteca.DAO_libro.seleccionar_todos", return_value=libros_mock):
            resultado = biblioteca.list_libros()
        self.assertEqual(resultado, libros_mock)
        self.assertEqual(biblioteca.bd, libros_mock)

    def test_list_libros_vacio(self):
        with patch("biblioteca.DAO_libro.seleccionar_todos", return_value=[]):
            resultado = biblioteca.list_libros()
        self.assertEqual(resultado, [])


class TestBuscarPorDisponibilidad(unittest.TestCase):
    """Cubre buscar_por_disponibilidad: disponibles, prestados, mezcla."""

    def _mock_libros(self):
        return [
            Libro(1, "A", "X", disponible=True),
            Libro(2, "B", "Y", disponible=False),
            Libro(3, "C", "Z", disponible=True),
        ]

    def test_buscar_disponibles_devuelve_solo_disponibles(self):
        with patch("biblioteca.DAO_libro.seleccionar_todos", return_value=self._mock_libros()):
            resultado = biblioteca.buscar_por_disponibilidad(True)
        self.assertEqual(len(resultado), 2)
        self.assertTrue(all(l.disponible for l in resultado))

    def test_buscar_prestados_devuelve_solo_prestados(self):
        with patch("biblioteca.DAO_libro.seleccionar_todos", return_value=self._mock_libros()):
            resultado = biblioteca.buscar_por_disponibilidad(False)
        self.assertEqual(len(resultado), 1)
        self.assertFalse(resultado[0].disponible)

    def test_sin_libros_devuelve_lista_vacia(self):
        with patch("biblioteca.DAO_libro.seleccionar_todos", return_value=[]):
            resultado = biblioteca.buscar_por_disponibilidad(True)
        self.assertEqual(resultado, [])


class TestBuscarPorTitulo(unittest.TestCase):
    """Cubre buscar_por_titulo: coincidencia exacta, mayúsculas, sin coincidencia."""

    def _mock_libros(self):
        return [
            Libro(1, "Quijote", "Cervantes"),
            Libro(2, "Odisea", "Homero"),
        ]

    def test_encuentra_libro_por_titulo_exacto(self):
        with patch("biblioteca.DAO_libro.seleccionar_todos", return_value=self._mock_libros()):
            resultado = biblioteca.buscar_por_titulo("Quijote")
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].titulo, "Quijote")

    def test_busqueda_insensible_a_mayusculas(self):
        with patch("biblioteca.DAO_libro.seleccionar_todos", return_value=self._mock_libros()):
            resultado = biblioteca.buscar_por_titulo("QUIJOTE")
        self.assertEqual(len(resultado), 1)

    def test_titulo_inexistente_devuelve_lista_vacia(self):
        with patch("biblioteca.DAO_libro.seleccionar_todos", return_value=self._mock_libros()):
            resultado = biblioteca.buscar_por_titulo("Inexistente")
        self.assertEqual(resultado, [])


class TestBuscarPorAutor(unittest.TestCase):
    """Cubre buscar_por_autor: coincidencia, mayúsculas, varios libros del mismo autor."""

    def _mock_libros(self):
        return [
            Libro(1, "Libro1", "Cervantes"),
            Libro(2, "Libro2", "Homero"),
            Libro(3, "Libro3", "Cervantes"),
        ]

    def test_encuentra_todos_los_libros_del_autor(self):
        with patch("biblioteca.DAO_libro.seleccionar_todos", return_value=self._mock_libros()):
            resultado = biblioteca.buscar_por_autor("Cervantes")
        self.assertEqual(len(resultado), 2)

    def test_busqueda_insensible_a_mayusculas(self):
        with patch("biblioteca.DAO_libro.seleccionar_todos", return_value=self._mock_libros()):
            resultado = biblioteca.buscar_por_autor("cervantes")
        self.assertEqual(len(resultado), 2)

    def test_autor_inexistente_devuelve_lista_vacia(self):
        with patch("biblioteca.DAO_libro.seleccionar_todos", return_value=self._mock_libros()):
            resultado = biblioteca.buscar_por_autor("Desconocido")
        self.assertEqual(resultado, [])

# ===========================================================================
# add_usuario
# ===========================================================================

class TestAddUsuario(TestBibliotecaBase):
    def test_agrega_usuario_exitosamente(self):
        usuario = Usuario(None, "Ana", "López", "ana@mail.com")
        biblioteca.usuarioDAO.add_usuario_bd = MagicMock(return_value=1)

        resultado = biblioteca.add_usuario(usuario)

        self.assertTrue(resultado)
        self.assertEqual(usuario.id, 1)
        self.assertEqual(biblioteca.ultimo_error, "")
        self.assertIn(usuario, biblioteca.usuarios)

    def test_error_al_agregar_usuario(self):
        usuario = Usuario(None, "Ana", "López", "ana@mail.com")
        biblioteca.usuarioDAO.add_usuario_bd = MagicMock(
            side_effect=Exception("DB error")
        )

        resultado = biblioteca.add_usuario(usuario)

        self.assertFalse(resultado)
        self.assertEqual(biblioteca.ultimo_error, "DB error")


# ===========================================================================
# remove_usuario
# ===========================================================================

class TestRemoveUsuario(TestBibliotecaBase):
    def test_elimina_usuario_existente(self):
        usuario = Usuario(1, "Ana", "López", "ana@mail.com")
        biblioteca.usuarios.append(usuario)
        biblioteca.usuarioDAO.get_usuario_id_bd = MagicMock(return_value=usuario)
        biblioteca.usuarioDAO.borrar_de_bd = MagicMock()

        resultado = biblioteca.remove_usuario(1)

        self.assertTrue(resultado)
        self.assertNotIn(usuario, biblioteca.usuarios)
        self.assertEqual(biblioteca.ultimo_error, "")

    def test_error_usuario_no_encontrado(self):
        biblioteca.usuarioDAO.get_usuario_id_bd = MagicMock(return_value=None)

        resultado = biblioteca.remove_usuario(99)

        self.assertFalse(resultado)
        self.assertEqual(biblioteca.ultimo_error, "Usuario no encontrado")

    def test_elimina_usuario_no_en_lista_local(self):
        """El usuario existe en BD pero no en la lista en memoria."""
        usuario = Usuario(5, "Bob", "Díaz", "bob@mail.com")
        biblioteca.usuarioDAO.get_usuario_id_bd = MagicMock(return_value=usuario)
        biblioteca.usuarioDAO.borrar_de_bd = MagicMock()

        resultado = biblioteca.remove_usuario(5)

        self.assertTrue(resultado)


# ===========================================================================
# get_usuario
# ===========================================================================

class TestGetUsuario(TestBibliotecaBase):
    def test_retorna_usuario_existente(self):
        usuario = Usuario(1, "Ana", "López", "ana@mail.com")
        biblioteca.usuarioDAO.get_usuario_id_bd = MagicMock(return_value=usuario)

        resultado = biblioteca.get_usuario(1)

        self.assertEqual(resultado, usuario)
        self.assertEqual(biblioteca.ultimo_error, "")

    def test_retorna_none_si_no_existe(self):
        biblioteca.usuarioDAO.get_usuario_id_bd = MagicMock(return_value=None)

        resultado = biblioteca.get_usuario(99)

        self.assertIsNone(resultado)
        self.assertEqual(biblioteca.ultimo_error, "Usuario no encontrado")


# ===========================================================================
# list_usuarios
# ===========================================================================

class TestListUsuarios(TestBibliotecaBase):
    def test_retorna_y_actualiza_lista(self):
        u1 = Usuario(1, "Ana", "López", "ana@mail.com")
        u2 = Usuario(2, "Luis", "Gómez", "luis@mail.com")
        biblioteca.usuarioDAO.seleccionar_todos = MagicMock(return_value=[u1, u2])

        resultado = biblioteca.list_usuarios()

        self.assertEqual(resultado, [u1, u2])
        self.assertEqual(biblioteca.usuarios, [u1, u2])

    def test_retorna_lista_vacia(self):
        biblioteca.usuarioDAO.seleccionar_todos = MagicMock(return_value=[])

        resultado = biblioteca.list_usuarios()

        self.assertEqual(resultado, [])


# ===========================================================================
# habilita_usuario
# ===========================================================================

class TestHabilitaUsuario(TestBibliotecaBase):
    def test_habilita_usuario_existente(self):
        usuario = Usuario(1, "Ana", "López", "ana@mail.com", habilitado=False)
        biblioteca.usuarios.append(usuario)
        biblioteca.usuarioDAO.get_usuario_id_bd = MagicMock(return_value=usuario)
        biblioteca.usuarioDAO.update_usuario_bd = MagicMock()

        resultado = biblioteca.habilita_usuario(1)

        self.assertTrue(resultado)
        self.assertTrue(usuario.habilitado)
        self.assertEqual(biblioteca.ultimo_error, "")

    def test_error_usuario_no_encontrado(self):
        biblioteca.usuarioDAO.get_usuario_id_bd = MagicMock(return_value=None)

        resultado = biblioteca.habilita_usuario(99)

        self.assertFalse(resultado)
        self.assertEqual(biblioteca.ultimo_error, "Usuario no encontrado")

    def test_error_excepcion_en_bd(self):
        biblioteca.usuarioDAO.get_usuario_id_bd = MagicMock(
            side_effect=Exception("fallo")
        )

        resultado = biblioteca.habilita_usuario(1)

        self.assertFalse(resultado)
        self.assertEqual(biblioteca.ultimo_error, "fallo")

    def test_habilita_usuario_no_en_lista_local(self):
        """Existe en BD pero no en la lista en memoria: no lanza excepción."""
        usuario = Usuario(7, "Ana", "López", "ana@mail.com", habilitado=False)
        biblioteca.usuarioDAO.get_usuario_id_bd = MagicMock(return_value=usuario)
        biblioteca.usuarioDAO.update_usuario_bd = MagicMock()

        resultado = biblioteca.habilita_usuario(7)

        self.assertTrue(resultado)


# ===========================================================================
# deshabilita_usuario
# ===========================================================================

class TestDeshabilitaUsuario(TestBibliotecaBase):
    def test_deshabilita_usuario_existente(self):
        usuario = Usuario(1, "Ana", "López", "ana@mail.com", habilitado=True)
        biblioteca.usuarios.append(usuario)
        biblioteca.usuarioDAO.get_usuario_id_bd = MagicMock(return_value=usuario)
        biblioteca.usuarioDAO.update_usuario_bd = MagicMock()

        resultado = biblioteca.deshabilita_usuario(1)

        self.assertTrue(resultado)
        self.assertFalse(usuario.habilitado)
        self.assertEqual(biblioteca.ultimo_error, "")

    def test_error_usuario_no_encontrado(self):
        biblioteca.usuarioDAO.get_usuario_id_bd = MagicMock(return_value=None)

        resultado = biblioteca.deshabilita_usuario(99)

        self.assertFalse(resultado)
        self.assertEqual(biblioteca.ultimo_error, "Usuario no encontrado")

    def test_error_excepcion_en_bd(self):
        biblioteca.usuarioDAO.get_usuario_id_bd = MagicMock(
            side_effect=Exception("fallo")
        )

        resultado = biblioteca.deshabilita_usuario(1)

        self.assertFalse(resultado)
        self.assertEqual(biblioteca.ultimo_error, "fallo")

    def test_deshabilita_usuario_no_en_lista_local(self):
        """Existe en BD pero no en la lista en memoria: no lanza excepción."""
        usuario = Usuario(8, "Ana", "López", "ana@mail.com", habilitado=True)
        biblioteca.usuarioDAO.get_usuario_id_bd = MagicMock(return_value=usuario)
        biblioteca.usuarioDAO.update_usuario_bd = MagicMock()

        resultado = biblioteca.deshabilita_usuario(8)

        self.assertTrue(resultado)


if __name__ == "__main__":
    unittest.main(verbosity=2)