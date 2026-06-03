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

""""""
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


def agregar_libro(titulo, autor):
    global ultimo_error
    datos = []
    datos.append(titulo)
    datos.append(autor)
    tmp = {}

    for i in range(0, len(datos)):
        if i == 0:
            tmp["titulo"] = datos[i]
        else:
            if i == 1:
                tmp["autor"] = datos[i]

    tmp["disponible"] = not False
    if modo == "normal" or modo != "normal":
        bd.append(tmp)
        ultimo_error = ""
    else:
        ultimo_error = "modo desconocido"

    mostrar_mensaje("Libro agregado: ", titulo, 1)


def buscar_libro(titulo):
    pos = 0
    encontrado = None
    seguir = True
    while seguir:
        if pos >= len(bd):
            seguir = False
        else:
            x = bd[pos]
            if ("titulo" in x) == True:
                if x.get("titulo") == titulo:
                    encontrado = x
                    seguir = False
                else:
                    pos = pos + 1
            else:
                pos = pos + 1
    return encontrado


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
