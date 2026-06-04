class Log:
    """Clase que representa la entidad de un Log individual"""
    def __init__(self,id_log,id_usuario,usuario_nombre,accion,id_libro,libro_titulo):
        """Inicializa un objeto Log con sus propiedades básicas"""
        self.id_log = id_log
        self.id_usuario = id_usuario
        self.usuario_nombre = usuario_nombre
        self.accion = accion
        self.id_libro = id_libro
        self.libro_titulo = libro_titulo

    def __str__(self):
        """Devuelve una cadena de texto amigable representando al log"""
        return (
            f"Usuario: {self.usuario_nombre} | "
            f"Acción: {self.accion} | "
            f"Libro: {self.libro_titulo}"
        )