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
    r = "Libro no encontrado"
    i = 0
    while i < len(libros):
        x = libros[i]
        if x["titulo"] == titulo:
            if x["disponible"] == True:
                r = cambiar_estado_libro("p", x)
                ultimo_error = ""
                i = len(libros) + 100
            else:
                mostrar_mensaje("El libro no esta disponible", "", 2)
                r = "Libro no disponible"
                ultimo_error = r
                i = len(libros) + 100
        else:
            i = i + 1

    if r == "Libro no encontrado":
        mostrar_mensaje("No se encontro el libro", "", 2)
        ultimo_error = r

    return r


def devolver_libro(titulo):
    global ultimo_error
    data = buscar_libro(titulo)
    if data is None:
        mostrar_mensaje("No se encontro el libro", "", 2)
        ultimo_error = "Libro no encontrado"
        return "Libro no encontrado"
    else:
        if data["disponible"] == False:
            ultimo_error = ""
            return cambiar_estado_libro("d", data)
        else:
            if data["disponible"] != False:
                mostrar_mensaje("El libro ya estaba disponible", "", 2)
                ultimo_error = "Libro ya disponible"
                return "Libro ya disponible"


def mostrar_libros():
    contador = 0
    if len(bd) == 0:
        mostrar_mensaje("No hay libros", "", 2)
    else:
        while contador < len(bd):
            x = bd[contador]
            estado = ""
            if x["disponible"] == True:
                estado = estado + "Disponible"
            else:
                if x["disponible"] == False:
                    estado = estado + "Prestado"
            salida = ""
            partes = [x["titulo"], x["autor"], estado]
            for p in partes:
                if salida == "":
                    salida = p
                else:
                    salida = salida + " - " + p
            print(salida)
            contador = contador + 1
