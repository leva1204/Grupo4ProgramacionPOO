"""Interfaz de consola para administrar pacientes."""
from getpass import getpass

from auxiliares.tablas import mostrar_tabla
from negocio.negocio_paciente import (
    crear_paciente,
    listar_pacientes,
    consultar_paciente,
    actualizar_paciente,
    eliminar_paciente,
)


def _mostrar(paciente):
    usuario = paciente.id_usuario
    print(f"\nID paciente: {paciente.id_usuario_id}")
    print(f"Nombre: {usuario.nombre}")
    print(f"Correo: {usuario.correo}")
    print(f"RUT: {paciente.rut}")
    print(f"Teléfono: {paciente.telefono or '-'}")
    print(f"ID dirección: {paciente.id_direccion_id}")


def solicitar_crear_paciente():
    print("\n--- Inscribir paciente ---")
    try:
        nombre = input("Nombre completo: ").strip()
        correo = input("Correo: ").strip()
        contrasena = getpass("Contraseña (mínimo 8 caracteres): ")
        rut = input("RUT: ").strip()
        telefono = input("Teléfono (opcional): ").strip() or None
        id_direccion = input("ID de dirección: ").strip()
        paciente = crear_paciente(
            nombre, correo, contrasena, rut, telefono, id_direccion
        )
        print(f"Paciente inscrito correctamente. ID: {paciente.id_usuario_id}")
    except Exception as exc:
        print(f"No se pudo inscribir el paciente: {exc}")


def solicitar_listar_paciente():
    try:
        pacientes = listar_pacientes()
        filas = [
            (
                paciente.id_usuario_id,
                paciente.id_usuario.nombre,
                paciente.id_usuario.correo,
                paciente.rut,
                paciente.telefono or "-",
                paciente.id_direccion_id,
            )
            for paciente in pacientes
        ]
        mostrar_tabla(
            "Pacientes registrados",
            ["ID", "Nombre", "Correo", "RUT", "Teléfono", "ID dirección"],
            filas,
            "No hay pacientes registrados.",
        )
    except Exception as exc:
        print(f"No se pudieron listar los pacientes: {exc}")


def solicitar_consultar_paciente():
    try:
        paciente = consultar_paciente(input("ID del paciente: ").strip())
        _mostrar(paciente)
    except Exception as exc:
        print(f"No se pudo consultar el paciente: {exc}")


def solicitar_actualizar_paciente():
    try:
        id_paciente = input("ID del paciente a modificar: ").strip()
        paciente = consultar_paciente(id_paciente)
        usuario = paciente.id_usuario
        print("Deje vacío un campo para conservar el valor actual.")
        nombre = input(f"Nombre [{usuario.nombre}]: ").strip() or None
        correo = input(f"Correo [{usuario.correo}]: ").strip() or None
        rut = input(f"RUT [{paciente.rut}]: ").strip() or None
        telefono = input(
            f"Teléfono [{paciente.telefono or '-'}]: "
        ).strip() or None
        id_direccion = input(
            f"ID dirección [{paciente.id_direccion_id}]: "
        ).strip() or None
        contrasena = getpass(
            "Nueva contraseña (vacío para conservar): "
        ) or None

        actualizar_paciente(
            id_paciente,
            nombre=nombre,
            correo=correo,
            rut=rut,
            telefono=telefono,
            id_direccion=id_direccion,
            contrasena=contrasena,
        )
        print("Paciente actualizado correctamente.")
    except Exception as exc:
        print(f"No se pudo actualizar el paciente: {exc}")


def solicitar_eliminar_paciente():
    try:
        id_paciente = input("ID del paciente a eliminar: ").strip()
        paciente = consultar_paciente(id_paciente)
        if input(
            f"¿Eliminar a {paciente.id_usuario.nombre}? [s/N]: "
        ).strip().lower() == "s":
            eliminar_paciente(id_paciente)
            print("Paciente eliminado.")
        else:
            print("Operación cancelada.")
    except Exception as exc:
        print(f"No se pudo eliminar el paciente: {exc}")
