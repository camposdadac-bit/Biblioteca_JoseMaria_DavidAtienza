from biblioteca import *
from DTO.Usuario import Usuario
from DTO.Libro import Libro

def menu_principal():
    while True:
        print("\n===== BIBLIOTECA =====")
        print("1. Gestión de libros")
        print("2. Gestión de usuarios")
        print("3. Préstamos")
        print("4. Logs")
        print("0. Salir")

        opcion = input("Elige opción: ")

        if opcion == "1":
            menu_libros()
        elif opcion == "2":
            menu_usuarios()
        elif opcion == "3":
            menu_prestamos()
        elif opcion == "4":
            menu_logs()
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción no válida")


def menu_libros():
    while True:
        print("\n--- LIBROS ---")
        print("1. Añadir libro")
        print("2. Eliminar libro")
        print("3. Listar libros")
        print("4. Buscar por título")
        print("5. Buscar por autor")
        print("0. Volver")

        opcion = input("Elige: ")

        if opcion == "1":
            titulo = input("Título: ")
            autor = input("Autor: ")
            isbn = input("ISBN: ")
            libro = Libro(None, titulo, autor, True, isbn)
            add_libro(libro)

        elif opcion == "2":
            id_libro = int(input("ID libro: "))
            remove_libro(id_libro)

        elif opcion == "3":
            libros = list_libros()
            for l in libros:
                print(simulacion_toString(l))

        elif opcion == "4":
            titulo = input("Título: ")
            res = buscar_por_titulo(titulo)
            for l in res:
                print(simulacion_toString(l))

        elif opcion == "5":
            autor = input("Autor: ")
            res = buscar_por_autor(autor)
            for l in res:
                print(simulacion_toString(l))

        elif opcion == "0":
            break


def menu_usuarios():
    while True:
        print("\n--- USUARIOS ---")
        print("1. Añadir usuario")
        print("2. Eliminar usuario")
        print("3. Listar usuarios")
        print("4. Habilitar usuario")
        print("5. Deshabilitar usuario")
        print("6. Buscar usuario por ID")
        print("0. Volver")

        opcion = input("Elige: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            apellidos = input("Apellidos: ")
            email = input("Email: ")
            u = Usuario(None, nombre, apellidos, email, True)
            add_usuario(u)

        elif opcion == "2":
            id_usuario = int(input("ID: "))
            remove_usuario(id_usuario)

        elif opcion == "3":
            usuarios = list_usuarios()
            for u in usuarios:
                print(u.nombre, u.apellidos, u.email)

        elif opcion == "4":
            id_usuario = int(input("ID: "))
            habilita_usuario(id_usuario)

        elif opcion == "5":
            id_usuario = int(input("ID: "))
            deshabilita_usuario(id_usuario)

        elif opcion == "6":
            id_usuario = int(input("ID: "))
            u = get_usuario(id_usuario)
            print(u)

        elif opcion == "0":
            break


def menu_prestamos():
    while True:
        print("\n--- PRÉSTAMOS ---")
        print("1. Prestar libro")
        print("2. Devolver libro")
        print("3. Ver estado libro")
        print("0. Volver")

        opcion = input("Elige: ")

        if opcion == "1":
            titulo = input("Título libro: ")
            id_usuario = int(input("ID usuario: "))
            prestar_libro(titulo, id_usuario)

        elif opcion == "2":
            titulo = input("Título libro: ")
            id_usuario = int(input("ID usuario: "))
            devolver_libro(titulo, id_usuario)

        elif opcion == "3":
            titulo = input("Título libro: ")
            libro = buscar_libro(titulo)
            if libro:
                print(obtener_estado(libro.disponible))
            else:
                print("No encontrado")

        elif opcion == "0":
            break


def menu_logs():
    while True:
        print("\n--- LOGS ---")
        print("1. Logs por usuario")
        print("2. Logs por libro")
        print("0. Volver")

        opcion = input("Elige: ")

        if opcion == "1":
            id_usuario = int(input("ID usuario: "))
            logs = get_logs_usuario(id_usuario)
            for l in logs:
                print(l)

        elif opcion == "2":
            id_libro = int(input("ID libro: "))
            logs = get_logs_libro(id_libro)
            for l in logs:
                print(l)

        elif opcion == "0":
            break


if __name__ == "__main__":
    menu_principal()