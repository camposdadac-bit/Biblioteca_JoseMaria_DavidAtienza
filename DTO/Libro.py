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

    def __getitem__(self, item):
        """Permite compatibilidad con código antiguo de tipo diccionario"""
        if item == "id": return self.id
        if item == "titulo": return self.titulo
        if item == "autor": return self.autor
        if item == "disponible": return self.disponible
        if item == "isbn": return self.isbn
        raise KeyError(item)

    def get(self, key, default=None):
        """Devuelve un atributo de forma segura imitando a un diccionario"""
        if key in ["id", "titulo", "autor", "disponible", "isbn"]:
            return getattr(self, key)
        return default