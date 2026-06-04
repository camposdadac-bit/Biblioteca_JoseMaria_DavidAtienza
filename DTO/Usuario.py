class Usuario:
    """Clase que representa la entidad de un Usuario individual"""
    def __init__(self, id, nombre, apellidos, email, habilitado=True):
        """Inicializa un objeto Usuario con sus propiedades básicas"""
        self.id = id
        self.nombre = nombre
        self.apellidos = apellidos
        self.email = email
        self.habilitado = habilitado

    def __str__(self):
        """Devuelve una cadena de texto amigable representando al usuario"""
        return f"{self.id} - {self.nombre} {self.apellidos} - {self.email} - {'Habilitado' if self.habilitado else 'Deshabilitado'}"