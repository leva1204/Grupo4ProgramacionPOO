from datetime import date, time, datetime
from peewee import IntegrityError
from datos.modelos.models import Usuario, Medico, Agenda, Horario
from datos.repositorios.repositorio_turno import RepositorioTurno

ESTADOS = {"Reservado", "Confirmado", "Atendido", "Cancelado"}
DIAS_FECHA = {
    0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves",
    4: "Viernes", 5: "Sábado", 6: "Domingo"
}
TRANSICIONES = {
    "Reservado": {"Confirmado", "Cancelado"},
    "Confirmado": {"Atendido", "Cancelado"},
    "Atendido": set(),
    "Cancelado": set(),
}


def _fecha(valor):
    if isinstance(valor, date) and not isinstance(valor, datetime):
        return valor
    try:
        return date.fromisoformat(str(valor).strip())
    except (ValueError, TypeError):
        raise ValueError("La fecha debe tener formato AAAA-MM-DD.")


def _hora(valor):
    if isinstance(valor, time):
        return valor
    try:
        return time.fromisoformat(str(valor).strip())
    except (ValueError, TypeError):
        raise ValueError("La hora debe tener formato HH:MM o HH:MM:SS.")


def _validar_referencias(id_paciente, id_medico, id_agenda):
    try:
        paciente = Usuario.get_or_none(Usuario.id_usuario == int(id_paciente))
        medico = Medico.get_or_none(Medico.id_usuario == int(id_medico))
        agenda = Agenda.get_or_none(Agenda.id_agenda == int(id_agenda))
    except (ValueError, TypeError):
        paciente = medico = agenda = None
    if paciente is None:
        raise ValueError("El paciente indicado no existe.")
    if medico is None:
        raise ValueError("El médico indicado no existe.")
    if agenda is None:
        raise ValueError("La agenda indicada no existe.")
    return paciente.id_usuario, medico.id_usuario, agenda.id_agenda


def _validar_disponibilidad(fecha, hora, id_medico, id_agenda, excluir=None):
    if fecha < date.today():
        raise ValueError("No se puede reservar un turno en una fecha pasada.")
    dia = DIAS_FECHA[fecha.weekday()]
    horarios = Horario.select().where(
        (Horario.dia == dia) &
        (Horario.id_medico == id_medico) &
        (Horario.id_agenda == id_agenda) &
        (Horario.disponible == True) &
        (Horario.horario_inicio <= hora) &
        (Horario.horario_fin > hora)
    )
    if not horarios.exists():
        raise ValueError(f"No hay horario disponible para ese médico y agenda el día {dia} a las {hora.strftime('%H:%M')}.")
    if RepositorioTurno.existe_reserva(fecha, hora, id_medico, excluir=excluir):
        raise ValueError("El médico ya tiene un turno reservado para esa fecha y hora.")


def crear_turno(fecha, hora, id_paciente, id_medico, id_agenda, estado="Reservado"):
    fecha, hora = _fecha(fecha), _hora(hora)
    if estado not in ESTADOS:
        raise ValueError("Estado no válido. Use: " + ", ".join(sorted(ESTADOS)) + ".")
    if estado != "Reservado":
        raise ValueError("Un turno nuevo debe crearse en estado 'Reservado'.")
    paciente_id, medico_id, agenda_id = _validar_referencias(id_paciente, id_medico, id_agenda)
    _validar_disponibilidad(fecha, hora, medico_id, agenda_id)
    try:
        return RepositorioTurno.guardar(fecha, hora, estado, paciente_id, medico_id, agenda_id)
    except IntegrityError as exc:
        raise ValueError("No se pudo registrar el turno; revise los datos relacionados.") from exc


def listar_turnos():
    return RepositorioTurno.listar()


def consultar_turno(id_turno):
    turno = RepositorioTurno.obtener(id_turno)
    if turno is None:
        raise ValueError("No se encontró el turno.")
    return turno


def actualizar_turno(id_turno, fecha=None, hora=None, id_paciente=None,
                     id_medico=None, id_agenda=None, estado=None):
    actual = consultar_turno(id_turno)
    nueva_fecha = _fecha(fecha) if fecha is not None else actual.fecha
    nueva_hora = _hora(hora) if hora is not None else actual.hora
    paciente_id = id_paciente if id_paciente is not None else actual.id_paciente_id
    medico_id = id_medico if id_medico is not None else actual.id_medico_id
    agenda_id = id_agenda if id_agenda is not None else actual.id_agenda_id
    paciente_id, medico_id, agenda_id = _validar_referencias(paciente_id, medico_id, agenda_id)
    nuevo_estado = estado if estado is not None else actual.estado
    if nuevo_estado not in ESTADOS:
        raise ValueError("Estado no válido.")
    if nuevo_estado != actual.estado and nuevo_estado not in TRANSICIONES[actual.estado]:
        raise ValueError(f"No se permite cambiar de '{actual.estado}' a '{nuevo_estado}'.")
    if nuevo_estado in {"Reservado", "Confirmado"}:
        _validar_disponibilidad(
            nueva_fecha, nueva_hora, medico_id, agenda_id, excluir=actual.id_turno
        )
    datos = {
        "fecha": nueva_fecha, "hora": nueva_hora, "estado": nuevo_estado,
        "id_paciente": paciente_id, "id_medico": medico_id, "id_agenda": agenda_id
    }
    try:
        RepositorioTurno.actualizar(actual.id_turno, datos)
        return consultar_turno(actual.id_turno)
    except IntegrityError as exc:
        raise ValueError("No se pudo actualizar el turno.") from exc


def eliminar_turno(id_turno):
    turno = consultar_turno(id_turno)
    try:
        RepositorioTurno.eliminar(turno.id_turno)
        return True
    except IntegrityError as exc:
        raise ValueError("No se pudo eliminar el turno.") from exc

listar_turno = listar_turnos
