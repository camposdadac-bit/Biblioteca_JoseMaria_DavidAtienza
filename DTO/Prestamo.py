class Prestamo:
    """Clase que representa la entidad de un Prestamo individual"""
    def __init__(self,id_prestamo,libro_id,usuario_id,fecha_prestamo=None,fecha_devolucion=None,estado="prestado"):
        """Inicializa un objeto Prestamo con sus propiedades básicas"""
        self.id_prestamo = id_prestamo
        self.libro_id = libro_id
        self.usuario_id = usuario_id
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion
    def __str__(self):
        """Devuelve una cadena de texto amigable representando al prestamo"""
        return (
            f"Prestamo {self.id_prestamo} | "
            f"Libro: {self.libro_id} | "
            f"Usuario: {self.usuario_id} | "
            f"Desde: {self.fecha_prestamo} | "
            f"Hasta: {self.fecha_devolucion}"
        )