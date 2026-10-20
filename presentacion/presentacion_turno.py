from auxiliares.tablas import mostrar_tabla
from negocio.negocio_turno import (
    crear_turno, listar_turnos, consultar_turno,
    actualizar_turno, eliminar_turno, ESTADOS
)


def _mostrar(turno):
    print(
        f"\nID: {turno.id_turno} | Fecha: {turno.fecha.isoformat()} | Hora: {turno.hora.strftime('%H:%M')} | "
        f"Estado: {turno.estado} | Paciente ID: {turno.id_paciente_id} | "
        f"Médico ID: {turno.id_medico_id} | Agenda ID: {turno.id_agenda_id}"
    )


def solicitar_crear_turno():
    print("\n--- Generar turno ---")
    try:
        fecha = input("Fecha (AAAA-MM-DD): ").strip()
        hora = input("Hora (HH:MM): ").strip()
        paciente = input("ID del paciente: ").strip()
        medico = input("ID del médico: ").strip()
        agenda = input("ID de agenda: ").strip()
        turno = crear_turno(fecha, hora, paciente, medico, agenda)
        print(f"Turno reservado correctamente. ID: {turno.id_turno}")
    except Exception as exc:
        print(f"No se pudo reservar el turno: {exc}")


def solicitar_listar_turno():
    try:
        turnos = listar_turnos()
        filas = [(turno.id_turno, turno.fecha.isoformat(), turno.hora.strftime("%H:%M"), turno.estado,
                  turno.id_paciente_id, turno.id_medico_id, turno.id_agenda_id) for turno in turnos]
        mostrar_tabla("Turnos registrados", ["ID", "Fecha", "Hora", "Estado", "ID paciente", "ID médico", "ID agenda"], filas, "No hay turnos registrados.")
    except Exception as exc:
        print(f"No se pudieron listar los turnos: {exc}")

def solicitar_consultar_turno():
    try:
        _mostrar(consultar_turno(input("ID del turno: ").strip()))
    except Exception as exc:
        print(f"No se pudo consultar el turno: {exc}")


def solicitar_actualizar_turno():
    try:
        id_turno = input("ID del turno a modificar: ").strip()
        turno = consultar_turno(id_turno)
        print("Deje vacío un campo para conservar su valor.")
        fecha = input(f"Fecha [{turno.fecha.isoformat()}]: ").strip() or None
        hora = input(f"Hora [{turno.hora.strftime('%H:%M')}]: ").strip() or None
        paciente = input(f"ID paciente [{turno.id_paciente_id}]: ").strip() or None
        medico = input(f"ID médico [{turno.id_medico_id}]: ").strip() or None
        agenda = input(f"ID agenda [{turno.id_agenda_id}]: ").strip() or None
        print("Estados permitidos:", ", ".join(sorted(ESTADOS)))
        estado = input(f"Estado [{turno.estado}]: ").strip() or None
        actualizar_turno(id_turno, fecha, hora, paciente, medico, agenda, estado)
        print("Turno actualizado correctamente.")
    except Exception as exc:
        print(f"No se pudo actualizar el turno: {exc}")


def solicitar_eliminar_turno():
    try:
        id_turno = input("ID del turno a eliminar: ").strip()
        turno = consultar_turno(id_turno)
        confirmar = input(f"¿Eliminar el turno {turno.id_turno} del {turno.fecha.isoformat()}? [s/N]: ").strip().lower()
        if confirmar == "s":
            eliminar_turno(id_turno)
            print("Turno eliminado.")
        else:
            print("Operación cancelada.")
    except Exception as exc:
        print(f"No se pudo eliminar el turno: {exc}")
