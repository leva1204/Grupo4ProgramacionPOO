from auxiliares.tablas import mostrar_tabla
from negocio.negocio_horario import (
    crear_horario, listar_horarios, consultar_horario,
    actualizar_horario, eliminar_horario
)


def _mostrar(horario):
    print(
        f"\nID: {horario.id_horario} | Día: {horario.dia} | "
        f"{horario.horario_inicio.strftime('%H:%M')} - {horario.horario_fin.strftime('%H:%M')} | "
        f"Disponible: {'Sí' if horario.disponible else 'No'} | "
        f"Agenda ID: {horario.id_agenda_id} | Médico ID: {horario.id_medico_id}"
    )


def solicitar_crear_horario():
    print("\n--- Crear horario ---")
    try:
        dia = input("Día de la semana: ").strip()
        inicio = input("Hora de inicio (HH:MM): ").strip()
        fin = input("Hora de término (HH:MM): ").strip()
        agenda = input("ID de agenda existente: ").strip()
        medico = input("ID de usuario del médico existente: ").strip()
        disponible = input("¿Disponible? [S/n]: ").strip().lower() != "n"
        horario = crear_horario(dia, inicio, fin, agenda, medico, disponible)
        print(f"Horario creado correctamente. ID: {horario.id_horario}")
    except Exception as exc:
        print(f"No se pudo crear el horario: {exc}")


def solicitar_listar_horario():
    try:
        horarios = listar_horarios()
        filas = [(
            horario.id_horario, horario.dia, horario.horario_inicio.strftime("%H:%M"),
            horario.horario_fin.strftime("%H:%M"), "Sí" if horario.disponible else "No",
            horario.id_agenda_id, horario.id_medico_id
        ) for horario in horarios]
        mostrar_tabla("Horarios registrados", ["ID", "Día", "Inicio", "Término", "Disponible", "ID agenda", "ID médico"], filas, "No hay horarios registrados.")
    except Exception as exc:
        print(f"No se pudieron listar los horarios: {exc}")

def solicitar_consultar_horario():
    try:
        _mostrar(consultar_horario(input("ID del horario: ").strip()))
    except Exception as exc:
        print(f"No se pudo consultar el horario: {exc}")


def solicitar_actualizar_horario():
    try:
        id_horario = input("ID del horario a modificar: ").strip()
        horario = consultar_horario(id_horario)
        print("Deje vacío un campo para conservar su valor.")
        dia = input(f"Día [{horario.dia}]: ").strip() or None
        inicio = input(f"Hora inicio [{horario.horario_inicio.strftime('%H:%M')}]: ").strip() or None
        fin = input(f"Hora término [{horario.horario_fin.strftime('%H:%M')}]: ").strip() or None
        agenda = input(f"ID agenda [{horario.id_agenda_id}]: ").strip() or None
        medico = input(f"ID médico [{horario.id_medico_id}]: ").strip() or None
        disponibilidad = input(f"Disponible [{'S' if horario.disponible else 'n'}] (S/n): ").strip().lower()
        disponible = (disponibilidad == "s") if disponibilidad else None
        actualizar_horario(id_horario, dia, inicio, fin, agenda, medico, disponible)
        print("Horario actualizado correctamente.")
    except Exception as exc:
        print(f"No se pudo actualizar el horario: {exc}")


def solicitar_eliminar_horario():
    try:
        id_horario = input("ID del horario a eliminar: ").strip()
        horario = consultar_horario(id_horario)
        confirmar = input(f"¿Eliminar horario {horario.dia} {horario.horario_inicio.strftime('%H:%M')}? [s/N]: ").strip().lower()
        if confirmar == "s":
            eliminar_horario(id_horario)
            print("Horario eliminado.")
        else:
            print("Operación cancelada.")
    except Exception as exc:
        print(f"No se pudo eliminar el horario: {exc}")
