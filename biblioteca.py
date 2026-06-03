from DTO.Libro import Libro
from DAO.DAO_libro import LibroDAO

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


"""DAO de libro con los 4 metodos crear, eliminar, listar, update """
def add_libro(libro):
    """Añade un objeto Libro a la base de datos de la biblioteca usando el DAO."""
    global ultimo_error
    try:
        """Llamamos a tu método pasándole los datos del objeto libro uno a uno"""
        nuevo_id = LibroDAO.insertar_en_bd(libro.titulo, libro.autor, libro.disponible, libro.isbn)
        """ Le asignamos al objeto libro el ID real que le dio SQLite"""
        libro.id = nuevo_id
        """ Lo guardamos en tu lista antigua 'bd' para mantener la compatibilidad en memoria"""
        bd.append(libro)
        ultimo_error = ""
        return True
    except Exception as e:
        """Si falla algo (por ejemplo, base de datos desconectada), guardamos el error"""
        ultimo_error = str(e)
        return False


def remove_libro(id_libro):
    """Elimina un libro de la biblioteca usando su identificador único."""
    global ultimo_error

    """Primero comprobamos si el libro existe de verdad usando tu método del DAO"""
    libro_existente = LibroDAO.seleccionar_por_id(id_libro)

    if libro_existente is None:
        ultimo_error = "Libro no encontrado"
        return False

    """Segundo si el libro existe, llamamos al DAO para que lo borre físicamente de la BD"""
    LibroDAO.borrar_de_bd(id_libro)

    """Tercero borramos de tu lista 'bd' antigua en memoria para que coincidan"""
    for l in bd:
        if l.id == id_libro:
           bd.remove(l)
           break

    ultimo_error = ""
    return True


def get_libro(id_libro):
    """Obtiene un libro específico mediante su ID desde la base de datos."""
    global ultimo_error
    """Le pedimos al DAO que busque ese libro por ID"""
    libro = LibroDAO.seleccionar_por_id(id_libro)

    if libro is None:
        ultimo_error = "Libro no encontrado"
        return None

    ultimo_error = ""
    return libro


def list_libros():
    """Devuelve la lista con todos los libros guardados en la base de datos."""
    global bd

    """Le pedimos al DAO que traiga todas las filas convertidas en objetos Libro"""
    todos_los_libros = LibroDAO.seleccionar_todos()

    """Sincronizamos tu lista 'bd' global con los datos reales de la base de datos"""
    bd = todos_los_libros

    return todos_los_libros


def buscar_por_disponibilidad(estado_disponible):
    """Busca libros según su estado: disponibles (True) o prestados (False)."""
    """Primero pedimos la lista actualizada de libros que viene de la base de datos"""
    todos = list_libros()

    """Segundo creamos una lista vacía en donde meteremos los que coincidan"""
    resultados = []

    """Tercero revisamos los libros uno por uno con un bucle for"""
    for l in todos:
        """Si la disponibilidad del libro es igual a la que busca el usuario:"""
        if l.disponible == estado_disponible:
            resultados.append(l)  # Guardamos el libro en nuestra lista

    """Por ultimo devolvemos la lista con los libros encontrados"""
    return resultados


def buscar_por_titulo(titulo_buscar):
    """Busca libros cuyo título coincida exactamente."""
    todos = list_libros()
    resultados = []

    for l in todos:
        """Usamos .lower() en ambos lados para que no importe si el usuario"""
        if l.titulo.lower() == titulo_buscar.lower():
            resultados.append(l)

    return resultados


def buscar_por_autor(autor_buscar):
    """Busca libros escritos por un autor específico."""
    todos = list_libros()
    resultados = []

    for l in todos:
        """Es la misma lógica que el título"""
        if l.autor.lower() == autor_buscar.lower():
            resultados.append(l)

    return resultados