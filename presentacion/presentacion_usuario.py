"""Interfaz de consola para administrar usuarios generales.

Los datos específicos del paciente (RUT, teléfono y dirección) se administran
exclusivamente desde la tabla y el módulo de pacientes.
"""
from getpass import getpass

from auxiliares.tablas import mostrar_tabla
from auxiliares.validaciones import validar_correo, validar_rut
from negocio.negocio_usuario import (
    TIPOS_USUARIO,
    crear_medico,
    crear_enfermero,
    listar_personal,
    obtener_perfil_personal,
    actualizar_personal,
    eliminar_personal,
)


def _mostrar_usuario(usuario, tipo, perfil):
    tipo_nombre = TIPOS_USUARIO.get(tipo, "Desconocido")
    if tipo == 1:
        detalle = (
            f"N° Formación: {perfil.numero_formacion} | "
            f"ID Especialidad: {perfil.id_especialidad_id}"
        )
    else:
        detalle = (
            f"RUT: {perfil.rut} | Teléfono: {perfil.telefono or '-'} | "
            f"Área: {perfil.area}"
        )
    print(
        f"\nID: {usuario.id_usuario} | Tipo: [{tipo}] {tipo_nombre} | "
        f"Nombre: {usuario.nombre} | Correo: {usuario.correo} | {detalle}"
    )
    


def solicitar_crear(id_tipo):
    singular = TIPOS_USUARIO[id_tipo]
    print(f"\n--- Crear {singular} ---")
    try:
        nombre = input("Nombre completo: ").strip()

        while True:
            correo = input("Correo (ej: usuario@dominio.com): ").strip()
            valido, mensaje = validar_correo(correo)
            if valido:
                break
            print(f"Correo inválido: {mensaje} Inténtelo de nuevo.\n")

        while True:
            contrasena = getpass("Contraseña (mínimo 8 caracteres): ")
            if len(contrasena) >= 8:
                break
            print("La contraseña debe tener al menos 8 caracteres.")

        if id_tipo == 1:
            numero_formacion = input("Número de formación: ").strip()
            id_especialidad = int(input("ID de especialidad: ").strip())
            registro = crear_medico(
                nombre, correo, contrasena, numero_formacion, id_especialidad
            )
            print(f"Médico creado correctamente. ID: {registro.id_usuario_id}")

        elif id_tipo == 2:
            while True:
                rut = input("RUT sin puntos (ej: 12345678-K): ").strip()
                if validar_rut(rut):
                    break
                print("RUT inválido. Ingréselo sin puntos y con guion (ej: 12345678-K).")

            telefono = input("Teléfono (opcional): ").strip() or None
            area = input("Área asignada (ej: Urgencias, Box, Toma de muestras): ").strip()
            registro = crear_enfermero(
                nombre, correo, contrasena, rut, telefono, area
            )
            print(f"Enfermero/a creado/a correctamente. ID: {registro.id_usuario_id}")

    except Exception as exc:
        print(f"No se pudo crear el registro: {exc}")


def solicitar_listar(id_tipo):
    try:
        registros = listar_personal(id_tipo)

        if id_tipo == 1:
            filas = [
                (
                    u.id_usuario,
                    u.nombre,
                    u.correo,
                    p.numero_formacion,
                    p.id_especialidad_id,
                )
                for u, _, p in registros
            ]
            mostrar_tabla(
                "Médicos registrados",
                ["ID", "Nombre", "Correo", "N° Formación", "ID Especialidad"],
                filas,
                "No hay médicos registrados.",
            )
        else:
            filas = [
                (
                    u.id_usuario,
                    u.nombre,
                    u.correo,
                    p.rut,
                    p.telefono or "-",
                    p.area,
                )
                for u, _, p in registros
            ]
            mostrar_tabla(
                "Enfermeros/as registrados/as",
                ["ID", "Nombre", "Correo", "RUT", "Teléfono", "Área"],
                filas,
                "No hay enfermeros/as registrados/as.",
            )
    except Exception as exc:
        print(f"No se pudo listar: {exc}")


def solicitar_consultar(id_tipo):
    rol = "médico" if id_tipo == 1 else "enfermero/a"
    print(f"\n--- Consultar {'Médico' if id_tipo == 1 else 'Enfermero/a'} ---")

    try:
        id_usuario = int(input(f"Ingrese ID del {rol}: ").strip())
    except ValueError:
        print("El ID debe ser un número.")
        return

    try:
        usuario, tipo, perfil = obtener_perfil_personal(id_usuario)
        if tipo != id_tipo or perfil is None:
            print(f"Esa ID de {rol} no existe.")
            return
        _mostrar_usuario(usuario, tipo, perfil)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"No se pudo consultar: {e}")

def solicitar_modificar(id_tipo):
    singular = TIPOS_USUARIO[id_tipo]
    print(f"\n--- Modificar {singular} ---")
    try:
        id_usuario = int(input(f"Ingrese ID del {singular.lower()} a modificar: ").strip())
        usuario, tipo, perfil = obtener_perfil_personal(id_usuario)

        if not usuario or tipo != id_tipo:
            print(f"No se encontró registro de {singular.lower()} con ese ID.")
            return

        _mostrar_usuario(usuario, tipo, perfil)
        print("\nIngrese los nuevos datos:")
        nombre = input("Nuevo nombre completo: ").strip()

        while True:
            correo = input("Nuevo correo: ").strip()
            valido, mensaje = validar_correo(correo)
            if valido:
                break
            print(f"Correo inválido: {mensaje}")

        if id_tipo == 1:
            telefono = None
            id_especialidad = int(input("Nuevo ID de especialidad: ").strip())
            area = None
        else:
            telefono = input("Nuevo teléfono (opcional): ").strip() or None
            area = input("Nueva área: ").strip()
            id_especialidad = None

        if id_tipo == 1:
            dato_extra = int(input("Nuevo ID de especialidad: ").strip())
        else:
            dato_extra = input("Nueva área asignada: ").strip()

        actualizar_personal(id_usuario, nombre, correo, telefono, dato_extra)
        print(f"{singular} actualizado/a correctamente.")

    except Exception as exc:
        print(f"No se pudo modificar: {exc}")


def solicitar_eliminar(id_tipo):
    singular = TIPOS_USUARIO[id_tipo]
    print(f"\n--- Eliminar {singular} ---")
    try:
        id_usuario = int(input(f"Ingrese ID del {singular.lower()} a eliminar: ").strip())
        usuario, tipo, perfil = obtener_perfil_personal(id_usuario)

        if not usuario or tipo != id_tipo:
            print(f"No se encontró registro de {singular.lower()} con ese ID.")
            return

        _mostrar_usuario(usuario, tipo, perfil)
        confirmar = input("\n¿Está seguro que desea eliminarlo? (s/n): ").strip().lower()
        if confirmar == "s":
            eliminar_personal(id_usuario)
            print(f"{singular} eliminado/a correctamente.")
        else:
            print("Operación cancelada.")

    except Exception as exc:
        print(f"No se pudo eliminar: {exc}")


def menu_gestion_personal(id_tipo):
    singular = "Médico" if id_tipo == 1 else "Enfermero/a"
    plural = "Médicos" if id_tipo == 1 else "Enfermeros/as"

    while True:
        print(f"\n[1] - Crear {singular}")
        print(f"[2] - Listar {plural}")
        print(f"[3] - Consultar {singular}")
        print(f"[4] - Modificar {singular}")
        print(f"[5] - Eliminar {singular}")
        print("[6] - Volver al menú anterior")

        opcion = input("\nIngrese su opción [1-6]: ").strip()

        if opcion == "1":
            solicitar_crear(id_tipo)
        elif opcion == "2":
            solicitar_listar(id_tipo)
        elif opcion == "3":
            solicitar_consultar(id_tipo)
        elif opcion == "4":
            solicitar_modificar(id_tipo)
        elif opcion == "5":
            solicitar_eliminar(id_tipo)
        elif opcion == "6":
            print("Volviendo al menú anterior.")
            break
        else:
            print("Opción inválida. Inténtelo de nuevo.")


def menu_usuarios():
    while True:
        print("\n--- Gestión de Usuarios ---")
        print("[1] - Médico")
        print("[2] - Enfermero/a")
        print("[3] - Volver al menú anterior")

        opcion = input("\nIngrese ID del tipo de usuario [1-3]: ").strip()

        if opcion == "1":
            menu_gestion_personal(1)
        elif opcion == "2":
            menu_gestion_personal(2)
        elif opcion == "3":
            print("Volviendo al menú anterior.")
            break
        else:
            print("Opción inválida. Inténtelo de nuevo.")