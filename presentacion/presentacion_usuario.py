"""Interfaz de consola para administrar usuarios generales.

Los datos específicos del paciente (RUT, teléfono y dirección) se administran
exclusivamente desde la tabla y el módulo de pacientes.
"""
from getpass import getpass

from auxiliares.tablas import mostrar_tabla
from negocio.negocio_usuario import (
    crear_usuario,
    listar_usuarios,
    consultar_usuario,
    actualizar_usuario,
    eliminar_usuario,
)


def _mostrar(usuario):
    print(
        f"\nID: {usuario.id_usuario} | Nombre: {usuario.nombre} "
        f"| Correo: {usuario.correo}"
    )


def solicitar_crear_usuario():
    try:
        usuario = crear_usuario(
            input("Nombre: ").strip(),
            input("Correo: ").strip(),
            getpass("Contraseña (mínimo 8 caracteres): "),
        )
        print(f"Usuario creado. ID: {usuario.id_usuario}")
    except Exception as exc:
        print(f"No se pudo crear el usuario: {exc}")


def solicitar_listar_usuario():
    try:
        usuarios = listar_usuarios()
        filas = [(usuario.id_usuario, usuario.nombre, usuario.correo) for usuario in usuarios]
        mostrar_tabla(
            "Usuarios registrados",
            ["ID", "Nombre", "Correo"],
            filas,
            "No hay usuarios registrados.",
        )
    except Exception as exc:
        print(f"No se pudieron listar los usuarios: {exc}")


def solicitar_consultar_usuario():
    try:
        _mostrar(consultar_usuario(input("ID usuario: ").strip()))
    except Exception as exc:
        print(f"No se pudo consultar el usuario: {exc}")


def solicitar_actualizar_usuario():
    try:
        id_usuario = input("ID usuario: ").strip()
        usuario = consultar_usuario(id_usuario)
        nombre = input(f"Nombre [{usuario.nombre}]: ").strip() or None
        correo = input(f"Correo [{usuario.correo}]: ").strip() or None
        contrasena = getpass(
            "Nueva contraseña (vacío para conservar): "
        ) or None
        actualizar_usuario(id_usuario, nombre, correo, contrasena)
        print("Usuario actualizado.")
    except Exception as exc:
        print(f"No se pudo actualizar el usuario: {exc}")


def solicitar_eliminar_usuario():
    try:
        id_usuario = input("ID usuario: ").strip()
        usuario = consultar_usuario(id_usuario)
        confirmar = input(
            f"¿Eliminar usuario {usuario.nombre}? [s/N]: "
        ).strip().lower()
        if confirmar == "s":
            eliminar_usuario(id_usuario)
            print("Usuario eliminado.")
        else:
            print("Operación cancelada.")
    except Exception as exc:
        print(f"No se pudo eliminar el usuario: {exc}")
