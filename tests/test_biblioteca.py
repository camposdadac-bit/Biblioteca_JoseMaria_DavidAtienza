import unittest
import biblioteca

class TestBiblioteca(unittest.TestCase):
    def setUp(self):
        biblioteca.libros.clear()
        biblioteca.ultimo_error = ""

    def test_agregar_libro_guarda_titulo_autor_y_estado_disponible(self):
        biblioteca.agregar_libro("El Quijote", "Miguel de Cervantes")

        self.assertEqual(len(biblioteca.libros), 1)
        self.assertEqual(biblioteca.libros[0]["titulo"], "El Quijote")
        self.assertEqual(biblioteca.libros[0]["autor"], "Miguel de Cervantes")
        self.assertTrue(biblioteca.libros[0]["disponible"])

    def test_prestar_libro_cambia_estado_si_existe_y_esta_disponible(self):
        biblioteca.agregar_libro("Nada", "Carmen Laforet")

        resultado = biblioteca.prestar_libro("Nada")

        self.assertEqual(resultado, "Libro prestado")
        self.assertFalse(biblioteca.libros[0]["disponible"])

    def test_devolver_libro_cambia_estado_si_estaba_prestado(self):
        biblioteca.agregar_libro("La colmena", "Camilo Jose Cela")
        biblioteca.prestar_libro("La colmena")

        resultado = biblioteca.devolver_libro("La colmena")

        self.assertEqual(resultado, "Libro devuelto")
        self.assertTrue(biblioteca.libros[0]["disponible"])

    def test_buscar_libro_existente_devuelve_diccionario(self):
        biblioteca.agregar_libro("Dune", "Frank Herbert")
        resultado = biblioteca.buscar_libro("Dune")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["titulo"], "Dune")

    def test_buscar_libro_inexistente_devuelve_none(self):
        resultado = biblioteca.buscar_libro("Libro Inexistente")
        self.assertIsNone(resultado)

    def test_prestar_libro_inexistente_devuelve_error(self):
        resultado = biblioteca.prestar_libro("No Existo")
        self.assertEqual(resultado, "Libro no encontrado")

    def test_prestar_libro_ya_prestado_devuelve_error(self):
        biblioteca.agregar_libro("El Hobbit", "J.R.R. Tolkien")
        biblioteca.prestar_libro("El Hobbit")
        resultado = biblioteca.prestar_libro("El Hobbit")
        self.assertEqual(resultado, "Libro no disponible")

    def test_devolver_libro_inexistente_devuelve_error(self):
        resultado = biblioteca.devolver_libro("Libro Falso")
        self.assertEqual(resultado, "Libro no encontrado")

    def test_devolver_libro_ya_disponible_devuelve_error(self):
        biblioteca.agregar_libro("Carmilla", "Sheridan Le Fanu")
        resultado = biblioteca.devolver_libro("Carmilla")
        self.assertEqual(resultado, "Libro ya disponible")

    def test_prestar_libro_inexistente_actualiza_ultimo_error(self):
        biblioteca.prestar_libro("El libro que no existe")
        self.assertEqual(biblioteca.ultimo_error, "Libro no encontrado")

    def test_prestar_libro_ya_prestado_actualiza_ultimo_error(self):
        biblioteca.agregar_libro("El Hobbit", "J.R.R. Tolkien")
        biblioteca.prestar_libro("El Hobbit")
        biblioteca.prestar_libro("El Hobbit")
        self.assertEqual(biblioteca.ultimo_error, "Libro no disponible")

    def test_devolver_libro_inexistente_actualiza_ultimo_error(self):
        biblioteca.devolver_libro("El libro fantasma")
        self.assertEqual(biblioteca.ultimo_error, "Libro no encontrado")

    def test_devolver_libro_ya_disponible_actualiza_ultimo_error(self):
        biblioteca.agregar_libro("Carmilla", "Sheridan Le Fanu")
        biblioteca.devolver_libro("Carmilla")
        self.assertEqual(biblioteca.ultimo_error, "Libro ya disponible")

    def test_mostrar_libros_cuando_la_biblioteca_esta_vacia(self):
        biblioteca.mostrar_libros()
        self.assertEqual(len(biblioteca.libros), 0)

    def test_mostrar_libros_con_ejemplares_disponibles_y_prestados(self):
        biblioteca.agregar_libro("Libro A", "Autor A")
        biblioteca.agregar_libro("Libro B", "Autor B")
        biblioteca.prestar_libro("Libro B")
        biblioteca.mostrar_libros()
        self.assertEqual(len(biblioteca.libros), 2)

    def test_cosa_imprime_string_con_c_distinto_de_1_y_2(self):
        biblioteca.mostrar_mensaje("Prueba c=0", tipo=0)

    def test_mover_devuelve_nada_si_accion_desconocida(self):
        resultado = biblioteca.cambiar_estado_libro("x", {})
        self.assertEqual(resultado, "Accion no reconocida")

    def test_buscar_libro_salta_registros_sin_clave_titulo(self):
        biblioteca.bd.append({"autor": "Anónimo", "disponible": True})
        resultado = biblioteca.buscar_libro("Cualquiera")
        self.assertIsNone(resultado)

if __name__ == "__main__":
    unittest.main()