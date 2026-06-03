from DTO.Libro import Libro
from crud.crud_libro import LibroDAO

libros = []
bd = libros
modo = "normal"
ultimo_error = ""
proximo_id = 1

"""muestra mensaje resutlado de realizar acciones del programa"""
def mostrar_mensaje(mensaje, titulo="", tipo=0):
    if tipo == 1:
        print(mensaje + titulo)
    elif tipo == 2:
        print(mensaje)
    else:
        print(str(mensaje))

"""Cambia el estado del libro a prestado o disponible para su prestación segun la accion requerida y el estado actual del libro"""
def cambiar_estado_libro(accion, libro):
    if accion == "prestar":
        libro["disponible"] = False
        mostrar_mensaje("Se presto el libro", tipo=2)
        return "Libro prestado"

    if accion == "devolver":
        libro["disponible"] = True
        mostrar_mensaje("Se devolvio el libro", tipo=2)
        return "Libro devuelto"

    return "Accion no reconocida"

"""Crea un libro con los atributos introducidos"""
def crear_libro(titulo, autor, isbn=None):
    global proximo_id

    nuevo_libro = Libro(proximo_id, titulo, autor, disponible=True, isbn=isbn)
    proximo_id += 1

    return nuevo_libro

"""Agrega el libro creado a la base de datos. Comprobando el modo actual(Ya veremos para que sirve)"""
def agregar_libro(titulo, autor, isbn=None):
    global ultimo_error

    if modo != "normal":
        ultimo_error = "modo desconocido"
        return

    nuevo_libro = crear_libro(titulo, autor,isbn)
    bd.append(nuevo_libro)
    ultimo_error = ""

    mostrar_mensaje("Libro agregado: ", titulo, 1)


"""Se encarga de buscar un libro especifico en la base de datos a través del titulo introducido"""
def buscar_libro(titulo):
    for libro in bd:
        if libro.get("titulo") == titulo:
            return libro
    return None

"""Revisa que el titulo introducido pertenece a un libro existente y disponible y en ese caso lo presta. Cambiando su estado a prestado con el metodo encargado de ello (cambiar_estado_libro)"""
def prestar_libro(titulo):
    global ultimo_error

    libro = buscar_libro(titulo)

    if libro is None:
        mostrar_mensaje("No se encontro el libro", tipo=2)
        ultimo_error = "Libro no encontrado"
        return "Libro no encontrado"

    if not libro["disponible"]:
        mostrar_mensaje("El libro no esta disponible", tipo=2)
        ultimo_error = "Libro no disponible"
        return "Libro no disponible"

    ultimo_error = ""
    return cambiar_estado_libro("prestar", libro)

"""Revisa que el titulo introducido pertenece a un libro existente y no disponible disponible. Para que en caso de que así sea, se cambie el estado del libro disponible con el metodo encargado de ello (cambiar_estado_libro)"""
def devolver_libro(titulo):
    global ultimo_error

    libro = buscar_libro(titulo)

    if libro is None:
        mostrar_mensaje("No se encontro el libro", tipo=2)
        ultimo_error = "Libro no encontrado"
        return "Libro no encontrado"

    if libro["disponible"]:
        mostrar_mensaje("El libro ya estaba disponible", tipo=2)
        ultimo_error = "Libro ya disponible"
        return "Libro ya disponible"

    ultimo_error = ""
    return cambiar_estado_libro("devolver", libro)

"""Metodo encargado de devolver el estado actual de un libro"""
def obtener_estado(disponible):
    return "Disponible" if disponible else "Prestado"

"""Una simulacion de lo que sería un ToString de un objeto"""
def simulacion_toString(libro):
    return (
        f"{libro['titulo']} - "
        f"{libro['autor']} - "
        f"{obtener_estado(libro['disponible'])}"
    )

"""Comprueba que la base de datos no esté vacia para mostrar su contenido. Muestra los libros usando el metodo ToString libro por libro"""
def mostrar_libros():
    if not bd:
        mostrar_mensaje("No hay libros", tipo=2)
        return

    for libro in bd:
        print(simulacion_toString(libro))

def add_libro(libro):
    """Añade un objeto Libro a la base de datos usando el DAO."""
    global ultimo_error
    try:
        LibroDAO.crear(libro)
        bd.append(libro)  # Sincronizamos con tu lista vieja por si acaso
        ultimo_error = ""
        return True
    except Exception as e:
        ultimo_error = str(e)
        return False

def remove_libro(id_libro):
    """Elimina un libro de la biblioteca por su ID a través del DAO."""
    global ultimo_error
    libro_existente = LibroDAO.obtener_por_id(id_libro)
    if libro_existente is None:
        ultimo_error = "Libro no encontrado"
        return False
    LibroDAO.eliminar(id_libro)
    ultimo_error = ""
    return True

def get_libro(id_libro):
    """Obtiene un libro específico mediante el DAO."""
    global ultimo_error
    libro = LibroDAO.obtener_por_id(id_libro)
    if libro is None:
        ultimo_error = "Libro no encontrado"
        return None
    ultimo_error = ""
    return libro

def list_libros():
    """Devuelve la lista con todos los libros traídos por el DAO."""
    global bd
    todos_los_libros = LibroDAO.obtener_todos()
    bd = todos_los_libros  # Actualizamos tu lista 'bd' global
    return todos_los_libros