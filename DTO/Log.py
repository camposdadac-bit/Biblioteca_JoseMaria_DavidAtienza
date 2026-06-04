class Log:

    def __init__(self,id_log,id_usuario,usuario_nombre,accion,id_libro,libro_titulo):
        self.id_log = id_log
        self.id_usuario = id_usuario
        self.usuario_nombre = usuario_nombre
        self.accion = accion
        self.id_libro = id_libro
        self.libro_titulo = libro_titulo

    def __str__(self):
        return (
            f"Usuario: {self.usuario_nombre} | "
            f"Acción: {self.accion} | "
            f"Libro: {self.libro_titulo}"
        )