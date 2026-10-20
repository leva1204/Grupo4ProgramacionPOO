import sys
from auxiliares import (
    nombre_aplicacion, version_aplicacion, menu_superior, menu_paciente,
    menu_horario, menu_turno, menu_direccion, menu_especialidad, menu_usuario, menu_medico, menu_agenda, opcion_invalida, menu_anterior
)
from presentacion.presentacion_turno import (
    solicitar_crear_turno, solicitar_listar_turno, solicitar_consultar_turno,
    solicitar_actualizar_turno, solicitar_eliminar_turno
)
from presentacion.presentacion_paciente import (
    solicitar_crear_paciente, solicitar_listar_paciente, solicitar_consultar_paciente,
    solicitar_actualizar_paciente, solicitar_eliminar_paciente
)
from presentacion.presentacion_horario import (
    solicitar_crear_horario, solicitar_listar_horario, solicitar_consultar_horario,
    solicitar_actualizar_horario, solicitar_eliminar_horario
)

from presentacion.presentacion_direccion import (
    solicitar_crear_direccion, solicitar_listar_direccion, solicitar_consultar_direccion, 
    solicitar_actualizar_direccion, solicitar_eliminar_direccion
)

from presentacion.presentacion_especialidad import (
    solicitar_crear_especialidad, solicitar_listar_especialidad, solicitar_consultar_especialidad,
    solicitar_actualizar_especialidad, solicitar_eliminar_especialidad
    )

from presentacion.presentacion_usuario import (
    solicitar_crear_usuario, solicitar_listar_usuario, solicitar_consultar_usuario, 
    solicitar_actualizar_usuario, solicitar_eliminar_usuario
    )

from presentacion.presentacion_medico import (
    solicitar_crear_medico, solicitar_listar_medico, solicitar_consultar_medico, 
    solicitar_actualizar_medico, solicitar_eliminar_medico
    )

from presentacion.presentacion_agenda import (
    solicitar_crear_agenda, solicitar_listar_agenda, solicitar_consultar_agenda, 
    solicitar_actualizar_agenda, solicitar_eliminar_agenda
    )


def _ejecutar_submenu(menu, acciones):
    while True:
        print()
        for clave, valor in menu.items():
            print(f"[{clave}] - {valor}")
        opcion = input(f"\nIngrese su opción [1-{len(menu)}]: ").strip()
        if opcion == str(len(menu)):
            print(menu_anterior)
            return
        accion = acciones.get(opcion)
        if accion:
            accion()
        else:
            print(opcion_invalida)


def menu_principal():
    print(f"\n{nombre_aplicacion} - {version_aplicacion}")
    print(f"{'=' * len(nombre_aplicacion)}==={'=' * len(version_aplicacion)}")
    acciones = {
        "1": lambda: _ejecutar_submenu(menu_turno, {
            "1": solicitar_crear_turno, "2": solicitar_listar_turno,
            "3": solicitar_consultar_turno, "4": solicitar_actualizar_turno,
            "5": solicitar_eliminar_turno
        }),
        "2": lambda: _ejecutar_submenu(menu_paciente, {
            "1": solicitar_crear_paciente, "2": solicitar_listar_paciente,
            "3": solicitar_consultar_paciente, "4": solicitar_actualizar_paciente,
            "5": solicitar_eliminar_paciente
        }),
        "3": lambda: _ejecutar_submenu(menu_horario, {
            "1": solicitar_crear_horario, "2": solicitar_listar_horario,
            "3": solicitar_consultar_horario, "4": solicitar_actualizar_horario,
            "5": solicitar_eliminar_horario
        }),
        "4": lambda: _ejecutar_submenu(menu_direccion, {
            "1": solicitar_crear_direccion, "2": solicitar_listar_direccion, 
            "3": solicitar_consultar_direccion, "4": solicitar_actualizar_direccion, 
            "5": solicitar_eliminar_direccion
        }),
        "5": lambda: _ejecutar_submenu(menu_especialidad, {
            "1": solicitar_crear_especialidad, "2": solicitar_listar_especialidad, 
            "3": solicitar_consultar_especialidad, "4": solicitar_actualizar_especialidad, 
            "5": solicitar_eliminar_especialidad
        }),
        "6": lambda: _ejecutar_submenu(menu_usuario, {
            "1": solicitar_crear_usuario, "2": solicitar_listar_usuario, 
            "3": solicitar_consultar_usuario, "4": solicitar_actualizar_usuario, 
            "5": solicitar_eliminar_usuario
        }),
        "7": lambda: _ejecutar_submenu(menu_medico, {
            "1": solicitar_crear_medico, "2": solicitar_listar_medico, 
            "3": solicitar_consultar_medico, "4": solicitar_actualizar_medico, 
            "5": solicitar_eliminar_medico
        }),
        "8": lambda: _ejecutar_submenu(menu_agenda, {
            "1": solicitar_crear_agenda, "2": solicitar_listar_agenda, 
            "3": solicitar_consultar_agenda, "4": solicitar_actualizar_agenda, 
            "5": solicitar_eliminar_agenda
        }),
        "9": lambda: sys.exit(f"Saliendo de {nombre_aplicacion}")
    }
    while True:
        print()
        for clave, valor in menu_superior.items():
            print(f"[{clave}] - {valor}")
        opcion = input("\nIngrese su opción [1-9]: ").strip()
        accion = acciones.get(opcion)
        if accion:
            accion()
        else:
            print(opcion_invalida)
