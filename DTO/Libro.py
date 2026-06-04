class Libro:
    """Clase que representa la entidad de un Libro individual"""

    def __init__(self, id_libro, titulo, autor, disponible=True, isbn=None):
        """Inicializa un objeto Libro con sus propiedades básicas"""
        self.id = id_libro
        self.titulo = titulo
        self.autor = autor
        self.disponible = disponible
        self.isbn = isbn

    def __str__(self):
        """Devuelve una cadena de texto amigable representando al libro"""
        estado = "Disponible" if self.disponible else "Prestado"
        return f"{self.titulo} - {self.autor} - {estado}"