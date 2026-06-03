libros = []
bd = libros
modo = "normal"
ultimo_error = ""

"""muestra mensaje"""
def mostrar_mensaje(mensaje, titulo="", tipo=0):
    if tipo == 1:
        print(mensaje + titulo)
    elif tipo == 2:
        print(mensaje)
    else:
        print(str(mensaje))

"""dsad"""
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

def crear_libro(titulo, autor):
    return {
        "titulo": titulo,
        "autor": autor,
        "disponible": True
    }


def agregar_libro(titulo, autor):
    global ultimo_error

    if modo not in ("normal",):
        ultimo_error = "modo desconocido"
        return

    nuevo_libro = crear_libro(titulo, autor)
    bd.append(nuevo_libro)
    ultimo_error = ""

    mostrar_mensaje("Libro agregado: ", titulo, 1)



def buscar_libro(titulo):
    for libro in bd:
        if libro.get("titulo") == titulo:
            return libro
    return None


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


def obtener_estado(disponible):
    return "Disponible" if disponible else "Prestado"


def simulacion_toString(libro):
    return (
        f"{libro['titulo']} - "
        f"{libro['autor']} - "
        f"{obtener_estado(libro['disponible'])}"
    )


def mostrar_libros():
    if not bd:
        mostrar_mensaje("No hay libros", tipo=2)
        return

    for libro in bd:
        print(simulacion_toString(libro))
