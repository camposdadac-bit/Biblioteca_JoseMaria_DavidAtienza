from biblioteca import usuarios

def buscar_por_nombre(nombre):
    resultados = []

    for usuario in usuarios:
        if usuario.nombre.lower() == nombre.lower():
            resultados.append(usuario)

    return resultados