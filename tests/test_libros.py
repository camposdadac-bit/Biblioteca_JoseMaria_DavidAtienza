import unittest
from DTO.Libro import Libro


class TestLibro(unittest.TestCase):

    def test_creacion_libro_con_parametros_obligatorios(self):
        libro = Libro(1, "1984", "George Orwell")

        self.assertEqual(libro.id, 1)
        self.assertEqual(libro.titulo, "1984")
        self.assertEqual(libro.autor, "George Orwell")
        self.assertTrue(libro.disponible)
        self.assertIsNone(libro.isbn)

    def test_creacion_libro_con_parametros_opcionales(self):
        libro = Libro(2, "Fahrenheit 451", "Ray Bradbury", disponible=False, isbn="978-X")

        self.assertFalse(libro.disponible)
        self.assertEqual(libro.isbn, "978-X")

    def test_str_representa_correctamente_libro_disponible(self):
        libro = Libro(1, "Dune", "Frank Herbert")
        self.assertEqual(str(libro), "Dune - Frank Herbert - Disponible")

    def test_str_representa_correctamente_libro_prestado(self):
        libro = Libro(1, "Dune", "Frank Herbert", disponible=False)
        self.assertEqual(str(libro), "Dune - Frank Herbert - Prestado")

    def test_compatibilidad_con_diccionarios_lectura(self):
        libro = Libro(1, "Fundación", "Isaac Asimov", isbn="12345")

        self.assertEqual(libro["titulo"], "Fundación")
        self.assertEqual(libro.get("autor"), "Isaac Asimov")
        self.assertEqual(libro["isbn"], "12345")
        self.assertTrue(libro["disponible"])

    def test_compatibilidad_con_diccionarios_escritura(self):
        libro = Libro(1, "El Hobbit", "J.R.R. Tolkien")
        libro["disponible"] = False
        libro["isbn"] = "000-111"

        self.assertFalse(libro.disponible)
        self.assertEqual(libro.isbn, "000-111")


if __name__ == "__main__":
    unittest.main()