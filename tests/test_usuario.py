import sqlite3
import unittest
from unittest.mock import patch
import sys
import os
import shutil
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from DTO.Usuario import Usuario
from DAO.UsuarioDAO import UsuarioDAO


# ===========================================================================
# Tests de Usuario
# ===========================================================================

class TestUsuario(unittest.TestCase):
    """Prueba la clase Usuario: que guarda bien los datos y que el texto
    sale en el formato correcto según si está habilitado o no"""

    def test_init_con_todos_los_parametros(self):
        """Al crear un usuario se guardan bien todos sus datos"""
        u = Usuario(1, "Ana", "López", "ana@mail.com", habilitado=False)
        self.assertEqual(u.id, 1)
        self.assertEqual(u.nombre, "Ana")
        self.assertEqual(u.apellidos, "López")
        self.assertEqual(u.email, "ana@mail.com")
        self.assertFalse(u.habilitado)

    def test_init_habilitado_por_defecto_es_true(self):
        """Si no dices si está habilitado o no, por defecto se crea habilitado"""
        u = Usuario(2, "Luis", "Gómez", "luis@mail.com")
        self.assertTrue(u.habilitado)

    def test_str_usuario_habilitado(self):
        """Al convertirlo a texto sale en el formato correcto cuando está habilitado"""
        u = Usuario(1, "Ana", "López", "ana@mail.com", habilitado=True)
        self.assertEqual(str(u), "1 - Ana López - ana@mail.com - Habilitado")

    def test_str_usuario_deshabilitado(self):
        """Al convertirlo a texto sale en el formato correcto cuando está deshabilitado"""
        u = Usuario(2, "Luis", "Gómez", "luis@mail.com", habilitado=False)
        self.assertEqual(str(u), "2 - Luis Gómez - luis@mail.com - Deshabilitado")


# ===========================================================================
# Tests de UsuarioDAO
# ===========================================================================

class TestUsuarioDAO(unittest.TestCase):
    """Prueba cada método del DAO contra una base de datos temporal,
    para que los tests no toquen la base de datos real"""

    def setUp(self):
        """Antes de cada test crea una base de datos falsa en una carpeta
        temporal del ordenador con la tabla usuarios vacía"""
        self.tmp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.tmp_dir) / "biblioteca.db"

        con = sqlite3.connect(self.db_path)
        con.execute(
            """
            CREATE TABLE usuarios (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre    TEXT    NOT NULL,
                apellidos TEXT    NOT NULL,
                email     TEXT    NOT NULL,
                habilitado INTEGER NOT NULL DEFAULT 1
            )
            """
        )
        con.commit()
        con.close()

        self.patcher = patch("DAO.UsuarioDAO.RUTA_BD", self.db_path)
        self.patcher.start()

        self.dao = UsuarioDAO()

    def tearDown(self):
        """Después de cada test borra la carpeta temporal. Si Windows no la
        deja borrar porque tiene el archivo bloqueado, espera un momento y
        lo intenta de nuevo. Si sigue sin poder, lo deja pasar para que no
        falle el test por culpa del sistema operativo"""
        self.patcher.stop()

        if hasattr(self, 'dao'):
            del self.dao

        try:
            shutil.rmtree(self.tmp_dir)
        except PermissionError:
            import gc
            gc.collect()
            try:
                shutil.rmtree(self.tmp_dir)
            except PermissionError:
                pass

    # -----------------------------------------------------------------------
    # add_usuario_bd
    # -----------------------------------------------------------------------

    def test_add_usuario_retorna_id(self):
        """Al insertar un usuario devuelve un ID válido"""
        u = Usuario(None, "Ana", "López", "ana@mail.com", habilitado=True)
        nuevo_id = self.dao.add_usuario_bd(u)
        self.assertIsInstance(nuevo_id, int)
        self.assertTrue(nuevo_id >= 1)

    def test_add_usuario_habilitado_false(self):
        """Si el usuario está deshabilitado se guarda correctamente como deshabilitado"""
        u = Usuario(None, "Bob", "Díaz", "bob@mail.com", habilitado=False)
        nuevo_id = self.dao.add_usuario_bd(u)
        recuperado = self.dao.get_usuario_id_bd(nuevo_id)
        self.assertFalse(recuperado.habilitado)

    # -----------------------------------------------------------------------
    # get_usuario_id_bd
    # -----------------------------------------------------------------------

    def test_get_usuario_existente(self):
        """Al buscar un usuario que existe devuelve sus datos correctos"""
        u = Usuario(None, "Ana", "López", "ana@mail.com")
        nuevo_id = self.dao.add_usuario_bd(u)
        resultado = self.dao.get_usuario_id_bd(nuevo_id)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.nombre, "Ana")
        self.assertEqual(resultado.apellidos, "López")
        self.assertEqual(resultado.email, "ana@mail.com")
        self.assertTrue(resultado.habilitado)

    def test_get_usuario_no_existente_retorna_none(self):
        """Si no existe devuelve None"""
        self.assertIsNone(self.dao.get_usuario_id_bd(9999))

    # -----------------------------------------------------------------------
    # seleccionar_todos
    # -----------------------------------------------------------------------

    def test_seleccionar_todos_retorna_lista(self):
        """Devuelve todos los usuarios insertados"""
        self.dao.add_usuario_bd(Usuario(None, "Ana", "López", "ana@mail.com"))
        self.dao.add_usuario_bd(Usuario(None, "Luis", "Gómez", "luis@mail.com"))
        todos = self.dao.seleccionar_todos()
        self.assertEqual(len(todos), 2)
        nombres = [u.nombre for u in todos]
        self.assertIn("Ana", nombres)
        self.assertIn("Luis", nombres)

    def test_seleccionar_todos_bd_vacia(self):
        """Si no hay ningún usuario devuelve una lista vacía"""
        self.assertEqual(self.dao.seleccionar_todos(), [])

    # -----------------------------------------------------------------------
    # update_usuario_bd
    # -----------------------------------------------------------------------

    def test_update_modifica_campos(self):
        """Al actualizar un usuario se guardan los nuevos datos"""
        u = Usuario(None, "Ana", "López", "ana@mail.com")
        nuevo_id = self.dao.add_usuario_bd(u)
        self.dao.update_usuario_bd(nuevo_id, "María", "Pérez", "maria@mail.com", False)
        actualizado = self.dao.get_usuario_id_bd(nuevo_id)
        self.assertEqual(actualizado.nombre, "María")
        self.assertEqual(actualizado.apellidos, "Pérez")
        self.assertEqual(actualizado.email, "maria@mail.com")
        self.assertFalse(actualizado.habilitado)

    def test_update_habilitado_a_true(self):
        """Se puede cambiar un usuario deshabilitado a habilitado"""
        u = Usuario(None, "Ana", "López", "ana@mail.com", habilitado=False)
        nuevo_id = self.dao.add_usuario_bd(u)
        self.dao.update_usuario_bd(nuevo_id, "Ana", "López", "ana@mail.com", True)
        actualizado = self.dao.get_usuario_id_bd(nuevo_id)
        self.assertTrue(actualizado.habilitado)

    # -----------------------------------------------------------------------
    # borrar_de_bd
    # -----------------------------------------------------------------------

    def test_borrar_usuario_existente(self):
        """Al borrar un usuario ya no se puede encontrar"""
        u = Usuario(None, "Ana", "López", "ana@mail.com")
        nuevo_id = self.dao.add_usuario_bd(u)
        self.dao.borrar_de_bd(nuevo_id)
        self.assertIsNone(self.dao.get_usuario_id_bd(nuevo_id))

    def test_borrar_id_inexistente_no_lanza_error(self):
        """Borrar un ID que no existe no da ningún error"""
        self.dao.borrar_de_bd(9999)

    # -----------------------------------------------------------------------
    # buscar_por_nombre_bd
    # -----------------------------------------------------------------------

    def test_buscar_por_nombre_encuentra_resultado(self):
        """Encuentra usuarios por nombre"""
        self.dao.add_usuario_bd(Usuario(None, "Ana", "López", "ana@mail.com"))
        resultados = self.dao.buscar_por_nombre_bd("Ana")
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0].nombre, "Ana")

    def test_buscar_por_nombre_insensible_mayusculas(self):
        """No importa si escribes el nombre en mayúsculas o minúsculas"""
        self.dao.add_usuario_bd(Usuario(None, "Ana", "López", "ana@mail.com"))
        resultados = self.dao.buscar_por_nombre_bd("ANA")
        self.assertEqual(len(resultados), 1)

    def test_buscar_por_nombre_sin_resultados(self):
        """Si no hay nadie con ese nombre devuelve lista vacía"""
        self.assertEqual(self.dao.buscar_por_nombre_bd("Fantasma"), [])

    def test_buscar_por_nombre_varios_resultados(self):
        """Devuelve todos si hay varios usuarios con el mismo nombre"""
        self.dao.add_usuario_bd(Usuario(None, "Ana", "López", "a1@mail.com"))
        self.dao.add_usuario_bd(Usuario(None, "Ana", "Gómez", "a2@mail.com"))
        resultados = self.dao.buscar_por_nombre_bd("ana")
        self.assertEqual(len(resultados), 2)

    # -----------------------------------------------------------------------
    # buscar_por_apellidos_bd
    # -----------------------------------------------------------------------

    def test_buscar_por_apellidos_encuentra_resultado(self):
        """Encuentra usuarios por apellidos"""
        self.dao.add_usuario_bd(Usuario(None, "Ana", "López", "ana@mail.com"))
        resultados = self.dao.buscar_por_apellidos_bd("López")
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0].apellidos, "López")

    def test_buscar_por_apellidos_insensible_mayusculas(self):
        """No importa si escribes los apellidos en mayúsculas o minúsculas"""
        self.dao.add_usuario_bd(Usuario(None, "Ana", "Garcia", "ana@mail.com"))
        resultados = self.dao.buscar_por_apellidos_bd("GARCIA")
        self.assertEqual(len(resultados), 1)

    def test_buscar_por_apellidos_sin_resultados(self):
        """Si no hay nadie con esos apellidos devuelve lista vacía"""
        self.assertEqual(self.dao.buscar_por_apellidos_bd("Desconocido"), [])

    def test_buscar_por_apellidos_varios_resultados(self):
        """Devuelve todos si hay varios usuarios con los mismos apellidos"""
        self.dao.add_usuario_bd(Usuario(None, "Ana", "García", "a1@mail.com"))
        self.dao.add_usuario_bd(Usuario(None, "Luis", "García", "l@mail.com"))
        resultados = self.dao.buscar_por_apellidos_bd("García")
        self.assertEqual(len(resultados), 2)

    # -----------------------------------------------------------------------
    # buscar_por_email_bd
    # -----------------------------------------------------------------------

    def test_buscar_por_email_encuentra_resultado(self):
        """Encuentra un usuario por email"""
        self.dao.add_usuario_bd(Usuario(None, "Ana", "López", "ana@mail.com"))
        resultado = self.dao.buscar_por_email_bd("ana@mail.com")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.email, "ana@mail.com")

    def test_buscar_por_email_insensible_mayusculas(self):
        """No importa si escribes el email en mayúsculas o minúsculas"""
        self.dao.add_usuario_bd(Usuario(None, "Ana", "López", "Ana@Mail.com"))
        resultado = self.dao.buscar_por_email_bd("ana@mail.com")
        self.assertIsNotNone(resultado)

    def test_buscar_por_email_no_encontrado_retorna_none(self):
        """Si no existe ningún usuario con ese email devuelve None"""
        self.assertIsNone(self.dao.buscar_por_email_bd("noexiste@mail.com"))


if __name__ == "__main__":
    unittest.main()