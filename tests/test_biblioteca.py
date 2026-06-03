"""
Tests para biblioteca.py — coº1bertura 100% (Versión unittest)
Cubre rutas exitosas y erróneas de todas las funciones.
"""
import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import io

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import biblioteca
from Usuario import Usuario


# ---------------------------------------------------------------------------
# Clase Base para Setup y Teardown (Reemplaza a la fixture de pytest)
# ---------------------------------------------------------------------------

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


# ===========================================================================
# mostrar_mensaje
# ===========================================================================

class TestMostrarMensaje(TestBibliotecaBase):
    def test_tipo_1_imprime_mensaje_y_titulo(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            biblioteca.mostrar_mensaje("Hola ", "Mundo", tipo=1)
            self.assertEqual(fake_out.getvalue().strip(), "Hola Mundo")

    def test_tipo_2_imprime_solo_mensaje(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            biblioteca.mostrar_mensaje("Solo mensaje", tipo=2)
            self.assertEqual(fake_out.getvalue().strip(), "Solo mensaje")

    def test_tipo_0_por_defecto_imprime_str(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            biblioteca.mostrar_mensaje(42)
            self.assertEqual(fake_out.getvalue().strip(), "42")

    def test_tipo_desconocido_imprime_str(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            biblioteca.mostrar_mensaje("x", tipo=99)
            self.assertEqual(fake_out.getvalue().strip(), "x")


# ===========================================================================
# obtener_estado
# ===========================================================================

class TestObtenerEstado(TestBibliotecaBase):
    def test_disponible_true(self):
        self.assertEqual(biblioteca.obtener_estado(True), "Disponible")

    def test_disponible_false(self):
        self.assertEqual(biblioteca.obtener_estado(False), "Prestado")


# ===========================================================================
# crear_libro
# ===========================================================================

class TestCrearLibro(TestBibliotecaBase):
    def test_crea_libro_con_campos_correctos(self):
        libro = biblioteca.crear_libro("1984", "Orwell")
        self.assertEqual(libro["titulo"], "1984")
        self.assertEqual(libro["autor"], "Orwell")
        self.assertTrue(libro["disponible"])


# ===========================================================================
# simulacion_toString
# ===========================================================================

class TestSimulacionToString(TestBibliotecaBase):
    def test_libro_disponible(self):
        libro = {"titulo": "Dune", "autor": "Herbert", "disponible": True}
        resultado = biblioteca.simulacion_toString(libro)
        self.assertEqual(resultado, "Dune - Herbert - Disponible")

    def test_libro_prestado(self):
        libro = {"titulo": "Dune", "autor": "Herbert", "disponible": False}
        resultado = biblioteca.simulacion_toString(libro)
        self.assertEqual(resultado, "Dune - Herbert - Prestado")


# ===========================================================================
# agregar_libro
# ===========================================================================

class TestAgregarLibro(TestBibliotecaBase):
    def test_agrega_libro_en_modo_normal(self):
        biblioteca.agregar_libro("El Quijote", "Cervantes")
        self.assertEqual(len(biblioteca.bd), 1)
        self.assertEqual(biblioteca.bd[0]["titulo"], "El Quijote")
        self.assertEqual(biblioteca.ultimo_error, "")

    def test_no_agrega_en_modo_desconocido(self):
        biblioteca.modo = "test"
        biblioteca.agregar_libro("El Quijote", "Cervantes")
        self.assertEqual(len(biblioteca.bd), 0)
        self.assertEqual(biblioteca.ultimo_error, "modo desconocido")

    def test_agrega_varios_libros(self):
        biblioteca.agregar_libro("Libro A", "Autor A")
        biblioteca.agregar_libro("Libro B", "Autor B")
        self.assertEqual(len(biblioteca.bd), 2)


# ===========================================================================
# buscar_libro
# ===========================================================================

class TestBuscarLibro(TestBibliotecaBase):
    def test_encuentra_libro_existente(self):
        biblioteca.agregar_libro("Hamlet", "Shakespeare")
        libro = biblioteca.buscar_libro("Hamlet")
        self.assertIsNotNone(libro)
        self.assertEqual(libro["titulo"], "Hamlet")

    def test_retorna_none_si_no_existe(self):
        self.assertIsNone(biblioteca.buscar_libro("Inexistente"))


# ===========================================================================
# cambiar_estado_libro
# ===========================================================================

class TestCambiarEstadoLibro(TestBibliotecaBase):
    def test_prestar_cambia_disponible_a_false(self):
        libro = {"titulo": "X", "autor": "Y", "disponible": True}
        resultado = biblioteca.cambiar_estado_libro("prestar", libro)
        self.assertFalse(libro["disponible"])
        self.assertEqual(resultado, "Libro prestado")

    def test_devolver_cambia_disponible_a_true(self):
        libro = {"titulo": "X", "autor": "Y", "disponible": False}
        resultado = biblioteca.cambiar_estado_libro("devolver", libro)
        self.assertTrue(libro["disponible"])
        self.assertEqual(resultado, "Libro devuelto")

    def test_accion_desconocida_retorna_mensaje(self):
        libro = {"titulo": "X", "autor": "Y", "disponible": True}
        resultado = biblioteca.cambiar_estado_libro("romper", libro)
        self.assertEqual(resultado, "Accion no reconocida")


# ===========================================================================
# prestar_libro
# ===========================================================================

class TestPrestarLibro(TestBibliotecaBase):
    def test_presta_libro_disponible(self):
        biblioteca.agregar_libro("Cien años", "García Márquez")
        resultado = biblioteca.prestar_libro("Cien años")
        self.assertEqual(resultado, "Libro prestado")
        self.assertEqual(biblioteca.ultimo_error, "")

    def test_error_libro_no_encontrado(self):
        resultado = biblioteca.prestar_libro("Inexistente")
        self.assertEqual(resultado, "Libro no encontrado")
        self.assertEqual(biblioteca.ultimo_error, "Libro no encontrado")

    def test_error_libro_ya_prestado(self):
        biblioteca.agregar_libro("Dune", "Herbert")
        biblioteca.prestar_libro("Dune")           # primer préstamo
        resultado = biblioteca.prestar_libro("Dune")  # intento duplicado
        self.assertEqual(resultado, "Libro no disponible")
        self.assertEqual(biblioteca.ultimo_error, "Libro no disponible")


# ===========================================================================
# devolver_libro
# ===========================================================================

class TestDevolverLibro(TestBibliotecaBase):
    def test_devuelve_libro_prestado(self):
        biblioteca.agregar_libro("Neuromancer", "Gibson")
        biblioteca.prestar_libro("Neuromancer")
        resultado = biblioteca.devolver_libro("Neuromancer")
        self.assertEqual(resultado, "Libro devuelto")
        self.assertEqual(biblioteca.ultimo_error, "")

    def test_error_libro_no_encontrado(self):
        resultado = biblioteca.devolver_libro("Fantasma")
        self.assertEqual(resultado, "Libro no encontrado")
        self.assertEqual(biblioteca.ultimo_error, "Libro no encontrado")

    def test_error_libro_ya_disponible(self):
        biblioteca.agregar_libro("Neuromancer", "Gibson")
        resultado = biblioteca.devolver_libro("Neuromancer")
        self.assertEqual(resultado, "Libro ya disponible")
        self.assertEqual(biblioteca.ultimo_error, "Libro ya disponible")


# ===========================================================================
# mostrar_libros
# ===========================================================================

class TestMostrarLibros(TestBibliotecaBase):
    def test_muestra_mensaje_si_bd_vacia(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            biblioteca.mostrar_libros()
            self.assertIn("No hay libros", fake_out.getvalue())

    def test_muestra_libros_existentes(self):
        biblioteca.agregar_libro("1984", "Orwell")
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            biblioteca.mostrar_libros()
            salida = fake_out.getvalue()
            self.assertIn("1984", salida)
            self.assertIn("Orwell", salida)


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
    unittest.main()