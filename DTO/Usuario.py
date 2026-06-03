class Usuario:
    def __init__(self, id, nombre, apellidos, email, habilitado=True):
        self.id = id
        self.nombre = nombre
        self.apellidos = apellidos
        self.email = email
        self.habilitado = habilitado

    def __str__(self):
        return f"{self.id} - {self.nombre} {self.apellidos} - {self.email} - {'Habilitado' if self.habilitado else 'Deshabilitado'}"