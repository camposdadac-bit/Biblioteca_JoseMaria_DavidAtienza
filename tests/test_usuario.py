"""
Tests para Usuario.py y UsuarioDAO.py — cobertura 100% (Versión unittest)
Ambas clases en el mismo archivo de test según lo solicitado.
"""
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
    def test_init_con_todos_los_parametros(self):
        u = Usuario(1, "Ana", "López", "ana@mail.com", habilitado=False)
        self.assertEqual(u.id, 1)
        self.assertEqual(u.nombre, "Ana")
        self.assertEqual(u.apellidos, "López")
        self.assertEqual(u.email, "ana@mail.com")
        self.assertFalse(u.habilitado)

    def test_init_habilitado_por_defecto_es_true(self):
        u = Usuario(2, "Luis", "Gómez", "luis@mail.com")
        self.assertTrue(u.habilitado)

    def test_str_usuario_habilitado(self):
        u = Usuario(1, "Ana", "López", "ana@mail.com", habilitado=True)
        self.assertEqual(str(u), "1 - Ana López - ana@mail.com - Habilitado")

    def test_str_usuario_deshabilitado(self):
        u = Usuario(2, "Luis", "Gómez", "luis@mail.com", habilitado=False)
        self.assertEqual(str(u), "2 - Luis Gómez - luis@mail.com - Deshabilitado")


# ===========================================================================
# Tests de UsuarioDAO
# ===========================================================================

class TestUsuarioDAO(unittest.TestCase):

    def setUp(self):
        """Reemplaza la fixture dao_con_bd de pytest para crear la BD temporal"""
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

        # Iniciamos el parche sobre RUTA_BD
        self.patcher = patch("DAO.UsuarioDAO.RUTA_BD", self.db_path)
        self.patcher.start()

        self.dao = UsuarioDAO()

    def tearDown(self):
        """Detiene el parche y limpia el directorio temporal de forma segura"""
        self.patcher.stop()

        # 1. Intentar limpiar cualquier rastro de conexiones en el DAO si fuera necesario
        if hasattr(self, 'dao'):
            del self.dao  # Elimina la instancia para forzar la liberación de recursos

        # 2. Borrar el directorio capturando el error de Windows si ocurre
        try:
            shutil.rmtree(self.tmp_dir)
        except PermissionError:
            # Si Windows se pone terco, le damos un instante o limpiamos los archivos internos primero
            import gc
            gc.collect()  # Forzamos al recolector de basura de Python a liberar residuos
            try:
                shutil.rmtree(self.tmp_dir)
            except PermissionError:
                pass  # Si aun así no puede, evita que el test falle por culpa del OS

    # -----------------------------------------------------------------------
    # add_usuario_bd
    # -----------------------------------------------------------------------

    def test_add_usuario_retorna_id(self):
        u = Usuario(None, "Ana", "López", "ana@mail.com", habilitado=True)
        nuevo_id = self.dao.add_usuario_bd(u)
        self.assertIsInstance(nuevo_id, int)
        self.assertTrue(nuevo_id >= 1)

    def test_add_usuario_habilitado_false(self):
        u = Usuario(None, "Bob", "Díaz", "bob@mail.com", habilitado=False)
        nuevo_id = self.dao.add_usuario_bd(u)
        recuperado = self.dao.get_usuario_id_bd(nuevo_id)
        self.assertFalse(recuperado.habilitado)

    # -----------------------------------------------------------------------
    # get_usuario_id_bd
    # -----------------------------------------------------------------------

    def test_get_usuario_existente(self):
        u = Usuario(None, "Ana", "López", "ana@mail.com")
        nuevo_id = self.dao.add_usuario_bd(u)
        resultado = self.dao.get_usuario_id_bd(nuevo_id)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.nombre, "Ana")
        self.assertEqual(resultado.apellidos, "López")
        self.assertEqual(resultado.email, "ana@mail.com")
        self.assertTrue(resultado.habilitado)

    def test_get_usuario_no_existente_retorna_none(self):
        self.assertIsNone(self.dao.get_usuario_id_bd(9999))

    # -----------------------------------------------------------------------
    # seleccionar_todos
    # -----------------------------------------------------------------------

    def test_seleccionar_todos_retorna_lista(self):
        self.dao.add_usuario_bd(Usuario(None, "Ana", "López", "ana@mail.com"))
        self.dao.add_usuario_bd(Usuario(None, "Luis", "Gómez", "luis@mail.com"))
        todos = self.dao.seleccionar_todos()
        self.assertEqual(len(todos), 2)
        nombres = [u.nombre for u in todos]
        self.assertIn("Ana", nombres)
        self.assertIn("Luis", nombres)

    def test_seleccionar_todos_bd_vacia(self):
        self.assertEqual(self.dao.seleccionar_todos(), [])

    # -----------------------------------------------------------------------
    # update_usuario_bd
    # -----------------------------------------------------------------------

    def test_update_modifica_campos(self):
        u = Usuario(None, "Ana", "López", "ana@mail.com")
        nuevo_id = self.dao.add_usuario_bd(u)
        self.dao.update_usuario_bd(nuevo_id, "María", "Pérez", "maria@mail.com", False)
        actualizado = self.dao.get_usuario_id_bd(nuevo_id)
        self.assertEqual(actualizado.nombre, "María")
        self.assertEqual(actualizado.apellidos, "Pérez")
        self.assertEqual(actualizado.email, "maria@mail.com")
        self.assertFalse(actualizado.habilitado)

    def test_update_habilitado_a_true(self):
        u = Usuario(None, "Ana", "López", "ana@mail.com", habilitado=False)
        nuevo_id = self.dao.add_usuario_bd(u)
        self.dao.update_usuario_bd(nuevo_id, "Ana", "López", "ana@mail.com", True)
        actualizado = self.dao.get_usuario_id_bd(nuevo_id)
        self.assertTrue(actualizado.habilitado)

    # -----------------------------------------------------------------------
    # borrar_de_bd
    # -----------------------------------------------------------------------

    def test_borrar_usuario_existente(self):
        u = Usuario(None, "Ana", "López", "ana@mail.com")
        nuevo_id = self.dao.add_usuario_bd(u)
        self.dao.borrar_de_bd(nuevo_id)
        self.assertIsNone(self.dao.get_usuario_id_bd(nuevo_id))

    def test_borrar_id_inexistente_no_lanza_error(self):
        self.dao.borrar_de_bd(9999)  # no debe lanzar excepción

    # -----------------------------------------------------------------------
    # buscar_por_nombre_bd
    # -----------------------------------------------------------------------

    def test_buscar_por_nombre_encuentra_resultado(self):
        self.dao.add_usuario_bd(Usuario(None, "Ana", "López", "ana@mail.com"))
        resultados = self.dao.buscar_por_nombre_bd("Ana")
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0].nombre, "Ana")

    def test_buscar_por_nombre_insensible_mayusculas(self):
        self.dao.add_usuario_bd(Usuario(None, "Ana", "López", "ana@mail.com"))
        resultados = self.dao.buscar_por_nombre_bd("ANA")
        self.assertEqual(len(resultados), 1)

    def test_buscar_por_nombre_sin_resultados(self):
        self.assertEqual(self.dao.buscar_por_nombre_bd("Fantasma"), [])

    def test_buscar_por_nombre_varios_resultados(self):
        self.dao.add_usuario_bd(Usuario(None, "Ana", "López", "a1@mail.com"))
        self.dao.add_usuario_bd(Usuario(None, "Ana", "Gómez", "a2@mail.com"))
        resultados = self.dao.buscar_por_nombre_bd("ana")
        self.assertEqual(len(resultados), 2)

    # -----------------------------------------------------------------------
    # buscar_por_apellidos_bd
    # -----------------------------------------------------------------------

    def test_buscar_por_apellidos_encuentra_resultado(self):
        self.dao.add_usuario_bd(Usuario(None, "Ana", "López", "ana@mail.com"))
        resultados = self.dao.buscar_por_apellidos_bd("López")
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0].apellidos, "López")

    def test_buscar_por_apellidos_insensible_mayusculas(self):
        self.dao.add_usuario_bd(Usuario(None, "Ana", "Garcia", "ana@mail.com"))
        resultados = self.dao.buscar_por_apellidos_bd("GARCIA")
        self.assertEqual(len(resultados), 1)

    def test_buscar_por_apellidos_sin_resultados(self):
        self.assertEqual(self.dao.buscar_por_apellidos_bd("Desconocido"), [])

    def test_buscar_por_apellidos_varios_resultados(self):
        self.dao.add_usuario_bd(Usuario(None, "Ana", "García", "a1@mail.com"))
        self.dao.add_usuario_bd(Usuario(None, "Luis", "García", "l@mail.com"))
        resultados = self.dao.buscar_por_apellidos_bd("García")
        self.assertEqual(len(resultados), 2)

    # -----------------------------------------------------------------------
    # buscar_por_email_bd
    # -----------------------------------------------------------------------

    def test_buscar_por_email_encuentra_resultado(self):
        self.dao.add_usuario_bd(Usuario(None, "Ana", "López", "ana@mail.com"))
        resultado = self.dao.buscar_por_email_bd("ana@mail.com")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.email, "ana@mail.com")

    def test_buscar_por_email_insensible_mayusculas(self):
        self.dao.add_usuario_bd(Usuario(None, "Ana", "López", "Ana@Mail.com"))
        resultado = self.dao.buscar_por_email_bd("ana@mail.com")
        self.assertIsNotNone(resultado)

    def test_buscar_por_email_no_encontrado_retorna_none(self):
        self.assertIsNone(self.dao.buscar_por_email_bd("noexiste@mail.com"))

if __name__ == "__main__":
    unittest.main()