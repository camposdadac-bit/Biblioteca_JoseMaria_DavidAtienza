from datetime import date, timedelta
from xmlrpc.client import DateTime

from DAO.LogDAO import LogDAO
from DAO.PrestamoDAO import PrestamoDAO
from DTO.Libro import Libro
from DAO.DAO_libro import DAO_libro
from DAO.PrestamoDAO import PrestamoDAO

from DAO.UsuarioDAO import UsuarioDAO

logDAO = LogDAO()
prestamoDAO = PrestamoDAO()
usuarioDAO = UsuarioDAO()
usuarios = []
libros = []
bd = libros
modo = "normal"
ultimo_error = ""
proximo_id = 1

    #=========================
    #FUNCIONES BIBLIOTECA
    #=========================

def mostrar_mensaje(mensaje, titulo="", tipo=0):
    """muestra mensaje resutlado de realizar acciones del programa"""
    if tipo == 1:
        print(mensaje + titulo)
    elif tipo == 2:
        print(mensaje)
    else:
        print(str(mensaje))

def cambiar_estado_libro(accion, libro, id_usuario):
    """Cambia el estado del libro a prestado o disponible para su prestación segun la accion requerida y el estado actual del libro"""
    usuarioaccion = usuarioDAO.get_usuario_id_bd(id_usuario)
    if accion == "prestar":
        libro.disponible = False
        DAO_libro.modificar_en_bd(libro.id,libro.titulo,libro.autor,False,libro.isbn)
        mostrar_mensaje("Se presto el libro", tipo=2)
        logDAO.insertar_log(id_usuario, usuarioaccion.nombre, "ha pedido prestado el libro", libro.id, libro.titulo)
        return "Libro prestado"

    if accion == "devolver":
        libro.disponible= True
        DAO_libro.modificar_en_bd(libro.id, libro.titulo, libro.autor, True, libro.isbn)
        mostrar_mensaje("Se devolvio el libro", tipo=2)
        logDAO.insertar_log(id_usuario,usuarioaccion.nombre,"ha devuelto el libro",libro.id,libro.titulo)
        return "Libro devuelto"

    return "Accion no reconocida"

def crear_libro(titulo, autor, isbn=None):
    """Crea un libro con los atributos introducidos"""
    global proximo_id

    nuevo_libro = Libro(proximo_id, titulo, autor, disponible=True, isbn=isbn)
    proximo_id += 1

    return nuevo_libro

def agregar_libro(titulo, autor, isbn=None):
    """Agrega el libro creado a la base de datos. Comprobando el modo actual(Ya veremos para que sirve)"""
    global ultimo_error

    if modo != "normal":
        ultimo_error = "modo desconocido"
        return

    nuevo_libro = crear_libro(titulo, autor,isbn)
    bd.append(nuevo_libro)
    ultimo_error = ""

    mostrar_mensaje("Libro agregado: ", titulo, 1)


def buscar_libro(titulo):
    """Se encarga de buscar un libro especifico en la base de datos a través del titulo introducido"""
    for libro in bd:
        if libro.titulo == titulo:
            return libro
    return None

def prestar_libro(titulo,id_usuario):
    """Revisa que el titulo introducido pertenece a un libro existente y disponible y en ese caso lo presta.
    Cambiando su estado a prestado con el metodo encargado de ello (cambiar_estado_libro)"""
    global ultimo_error
    usuarioprestacion = usuarioDAO.get_usuario_id_bd(id_usuario)
    if usuarioprestacion is None:
        return None
    libro = buscar_libro(titulo)
    fechaactual = date.today()
    fechadevolucion = fechaactual+timedelta(days=30)
    if libro is None:
        mostrar_mensaje("No se encontro el libro", tipo=2)
        ultimo_error = "Libro no encontrado"
        return "Libro no encontrado"

    prestado = prestamoDAO.tiene_prestamo_activo(libro.id)

    if prestado:
        mostrar_mensaje("El libro no esta disponible", tipo=2)
        ultimo_error = "Libro no disponible"
        return "Libro no disponible"

    prestamoDAO.registrar_prestamo(libro.id,id_usuario,fechaactual,fechadevolucion)
    ultimo_error = ""
    return cambiar_estado_libro("prestar", libro, id_usuario)

def devolver_libro(titulo,id_usuario):
    """Revisa que el titulo introducido pertenece a un libro existente y no disponible disponible.
    Para que en caso de que así sea, se cambie el estado del libro disponible con el metodo encargado de ello (cambiar_estado_libro)"""
    global ultimo_error
    usuarioprestacion = usuarioDAO.get_usuario_id_bd(id_usuario)
    if usuarioprestacion is None:
        return None

    libro = buscar_libro(titulo)

    if libro is None:
        mostrar_mensaje("No se encontro el libro", tipo=2)
        ultimo_error = "Libro no encontrado"
        return "Libro no encontrado"

    if not PrestamoDAO().tiene_prestamo_activo(libro.id):
        mostrar_mensaje("El libro ya estaba disponible", tipo=2)
        ultimo_error = "Libro ya disponible"
        return "Libro ya disponible"

    PrestamoDAO().devolver_prestamo(libro.id)
    ultimo_error = ""
    return cambiar_estado_libro("devolver", libro, id_usuario)

def obtener_estado(disponible):
    """Metodo encargado de devolver el estado actual de un libro"""
    return "Disponible" if disponible else "Prestado"

def simulacion_toString(libro):
    """Una simulacion de lo que sería un ToString de un objeto"""
    return (
        f"{libro['titulo']} - "
        f"{libro['autor']} - "
        f"{obtener_estado(libro['disponible'])}"
    )

def mostrar_libros():
    """Comprueba que la base de datos no esté vacia para mostrar su contenido. Muestra los libros usando el metodo ToString libro por libro"""
    if not bd:
        mostrar_mensaje("No hay libros", tipo=2)
        return

    for libro in bd:
        print(simulacion_toString(libro))

# =========================
# FUNCIONES USUARIO
# =========================

def add_usuario(usuario):
    """Añade un usuario a la BD y a la lista en memoria, si falla guarda el error y devuelve False."""
    global ultimo_error

    try:
        nuevo_id = usuarioDAO.add_usuario_bd(usuario)

        usuario.id = nuevo_id
        usuarios.append(usuario)
        ultimo_error = ""
        return True

    except Exception as e:
        ultimo_error = str(e)
        return False


def remove_usuario(id_usuario):
    """Elimina un usuario de la BD y de la lista en memoria.
    Si no existe devuelve False, si existe en BD pero no en la lista
    en memoria el for no encuentra nada y no rompe"""
    global ultimo_error

    usuario_existente = usuarioDAO.get_usuario_id_bd(id_usuario)

    if usuario_existente is None:
        ultimo_error = "Usuario no encontrado"
        return False

    usuarioDAO.borrar_de_bd(id_usuario)

    for usuario in usuarios:
        if usuario.id == id_usuario:
            usuarios.remove(usuario)
            break

    ultimo_error = ""
    return True


def get_usuario(id_usuario):
    """Obtiene un usuario por ID desde la BD.
    Si no existe guarda el error y devuelve None"""
    global ultimo_error

    usuario = usuarioDAO.get_usuario_id_bd(id_usuario)

    if usuario is None:
        ultimo_error = "Usuario no encontrado"
        return None

    ultimo_error = ""
    return usuario


def list_usuarios():
    """Trae todos los usuarios de la BD y sincroniza la lista en memoria"""
    global usuarios

    todos_los_usuarios = usuarioDAO.seleccionar_todos()

    usuarios = todos_los_usuarios

    return todos_los_usuarios


def habilita_usuario(id_usuario):
    """Pone habilitado=False en la BD y en la lista en memoria.
    Si no existe devuelve False, si falla por excepción guarda el error
    devuelve False. Si existe en BD pero no en la lista el bucle no
    encuentra nada y no rompe"""
    global ultimo_error

    try:
        usuario = usuarioDAO.get_usuario_id_bd(id_usuario)

        if usuario is None:
            ultimo_error = "Usuario no encontrado"
            return False

        usuarioDAO.update_usuario_bd(id_usuario, usuario.nombre, usuario.apellidos, usuario.email, True)

        for u in usuarios:
            if u.id == id_usuario:
                u.habilitado = True
                break

        ultimo_error = ""
        return True

    except Exception as e:
        ultimo_error = str(e)
        return False


def deshabilita_usuario(id_usuario):
    """Pone habilitado=False en la BD y en la lista en memoria.
    Si no existe devuelve False, si falla por excepción guarda el error
    devuelve False. Si existe en BD pero no en la lista el bucle no
    encuentra nada y no rompe"""
    global ultimo_error

    try:
        usuario = usuarioDAO.get_usuario_id_bd(id_usuario)

        if usuario is None:
            ultimo_error = "Usuario no encontrado"
            return False

        usuarioDAO.update_usuario_bd(id_usuario, usuario.nombre, usuario.apellidos, usuario.email, False)

        for u in usuarios:
            if u.id == id_usuario:
                u.habilitado = False
                break

        ultimo_error = ""
        return True

    except Exception as e:
        ultimo_error = str(e)
        return False
    #=========================
    #FUNCIONES LIBRO
    #=========================
"""DAO de libro con los 4 metodos crear, eliminar, listar, update """

def add_libro(libro):
    """Añade un objeto Libro a la base de datos de la biblioteca usando el DAO"""
    global ultimo_error
    try:
        """Llamamos a tu método pasándole los datos"""
        nuevo_id = DAO_libro.insertar_en_bd(libro.titulo, libro.autor, libro.disponible, libro.isbn)
        libro.id = nuevo_id
        bd.append(libro)
        ultimo_error = ""
        return True
    except Exception as e:
        """Si falla guardamos el error"""
        ultimo_error = str(e)
        return False


def remove_libro(id_libro):
    """Elimina un libro de la biblioteca usando su identificador único"""
    global ultimo_error

    """Primero comprobamos si el libro existe"""
    libro_existente = DAO_libro.seleccionar_por_id(id_libro)

    if libro_existente is None:
        ultimo_error = "Libro no encontrado"
        return False

    """Segundo si el libro existe, llamamos al DAO para que lo borre físicamente de la BD"""
    DAO_libro.borrar_de_bd(id_libro)

    """Tercero borramos de tu lista 'bd' antigua en memoria para que coincidan"""
    for l in bd:
        if l.id == id_libro:
           bd.remove(l)
           break

    ultimo_error = ""
    return True


def get_libro(id_libro):
    """Obtiene un libro específico mediante su ID desde la base de datos"""
    global ultimo_error
    """Le pedimos al DAO que busque ese libro por ID"""
    libro = DAO_libro.seleccionar_por_id(id_libro)

    if libro is None:
        ultimo_error = "Libro no encontrado"
        return None

    ultimo_error = ""
    return libro


def list_libros():
    """Devuelve la lista con todos los libros guardados en la base de datos"""
    global bd

    """Le pedimos al DAO que traiga todas las filas convertidas en objetos Libro"""
    todos_los_libros = DAO_libro.seleccionar_todos()

    """Sincronizamos tu lista 'bd' global con los datos reales de la base de datos"""
    bd = todos_los_libros

    return todos_los_libros


def buscar_por_disponibilidad(estado_disponible):
    """Busquedas obligatorias"""
    """Busca libros según su estado: disponibles o prestados"""
    """Primero pedimos la lista actualizada de libros que viene de la base de datos"""
    todos = list_libros()

    """Segundo creamos una lista vacía en donde meteremos los que coincidan"""
    resultados = []

    """Tercero revisamos los libros"""
    for l in todos:
        """Si la disponibilidad del libro es igual a la que busca el usuario"""
        if l.disponible == estado_disponible:
            resultados.append(l)
            """Guardamos el libro en nuestra lista"""

    """Devolvemos los libros encontrados"""
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

def get_logs_usuario(id_usuario):
    """Obtiene los logs por ususario"""
    global ultimo_error

    try:
        logs = logDAO.obtener_logs_por_usuario(id_usuario)

        ultimo_error = ""
        return logs

    except Exception as e:
        ultimo_error = str(e)
        return []

def get_logs_libro(id_libro):
    """Obtiene los logs por libros"""
    global ultimo_error

    try:
        logs = logDAO.obtener_logs_por_libro(id_libro)

        ultimo_error = ""
        return logs

    except Exception as e:
        ultimo_error = str(e)
        return []