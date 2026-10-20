from datetime import time
from peewee import IntegrityError
from datos.modelos.models import Agenda, Medico, Turno
from datos.repositorios.repositorio_horario import RepositorioHorario

DIAS = {
    "lunes": "Lunes", "martes": "Martes", "miercoles": "Miércoles",
    "miércoles": "Miércoles", "jueves": "Jueves", "viernes": "Viernes",
    "sabado": "Sábado", "sábado": "Sábado", "domingo": "Domingo"
}


def _hora(valor):
    if isinstance(valor, time):
        return valor
    try:
        return time.fromisoformat(str(valor).strip())
    except (ValueError, TypeError):
        raise ValueError("La hora debe tener formato HH:MM o HH:MM:SS.")


def _validar_referencias(id_agenda, id_medico):
    try:
        agenda = Agenda.get_or_none(Agenda.id_agenda == int(id_agenda))
        medico = Medico.get_or_none(Medico.id_usuario == int(id_medico))
    except (ValueError, TypeError):
        agenda = medico = None
    if agenda is None:
        raise ValueError("La agenda indicada no existe.")
    if medico is None:
        raise ValueError("El médico indicado no existe.")
    return agenda.id_agenda, medico.id_usuario


def crear_horario(dia, horario_inicio, horario_fin, id_agenda, id_medico, disponible=True):
    dia_ingresado = (dia or "").strip().lower()
    if dia_ingresado not in DIAS:
        raise ValueError("Ingrese un día válido de la semana.")
    dia = DIAS[dia_ingresado]
    inicio, fin = _hora(horario_inicio), _hora(horario_fin)
    if inicio >= fin:
        raise ValueError("La hora de inicio debe ser anterior a la hora de término.")
    id_agenda, id_medico = _validar_referencias(id_agenda, id_medico)
    if RepositorioHorario.buscar_solapamiento(dia, inicio, fin, id_medico, id_agenda):
        raise ValueError("El horario se superpone con otro horario del mismo médico y agenda.")
    try:
        return RepositorioHorario.guardar(dia, inicio, fin, bool(disponible), id_agenda, id_medico)
    except IntegrityError as exc:
        raise ValueError("No se pudo guardar el horario; verifique médico y agenda.") from exc


def listar_horarios():
    return RepositorioHorario.listar()


def consultar_horario(id_horario):
    horario = RepositorioHorario.obtener(id_horario)
    if horario is None:
        raise ValueError("No se encontró el horario.")
    return horario


def actualizar_horario(id_horario, dia=None, horario_inicio=None, horario_fin=None,
                        id_agenda=None, id_medico=None, disponible=None):
    actual = consultar_horario(id_horario)
    nuevo_dia = actual.dia
    if dia is not None:
        clave = dia.strip().lower()
        if clave not in DIAS:
            raise ValueError("Ingrese un día válido de la semana.")
        nuevo_dia = DIAS[clave]
    inicio = _hora(horario_inicio) if horario_inicio is not None else actual.horario_inicio
    fin = _hora(horario_fin) if horario_fin is not None else actual.horario_fin
    if inicio >= fin:
        raise ValueError("La hora de inicio debe ser anterior a la hora de término.")
    agenda_id = id_agenda if id_agenda is not None else actual.id_agenda_id
    medico_id = id_medico if id_medico is not None else actual.id_medico_id
    agenda_id, medico_id = _validar_referencias(agenda_id, medico_id)
    if RepositorioHorario.buscar_solapamiento(
        nuevo_dia, inicio, fin, medico_id, agenda_id, excluir=actual.id_horario
    ):
        raise ValueError("El horario se superpone con otro horario del mismo médico y agenda.")
    datos = {
        "dia": nuevo_dia, "horario_inicio": inicio, "horario_fin": fin,
        "id_agenda": agenda_id, "id_medico": medico_id
    }
    if disponible is not None:
        datos["disponible"] = bool(disponible)
    try:
        RepositorioHorario.actualizar(actual.id_horario, datos)
        return consultar_horario(actual.id_horario)
    except IntegrityError as exc:
        raise ValueError("No se pudo actualizar el horario.") from exc


def eliminar_horario(id_horario):
    horario = consultar_horario(id_horario)
    dias_por_numero = {
        0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves",
        4: "Viernes", 5: "Sábado", 6: "Domingo"
    }
    turnos_relacionados = Turno.select().where(
        (Turno.id_agenda == horario.id_agenda_id) &
        (Turno.id_medico == horario.id_medico_id)
    )
    existe_turno_en_horario = any(
        dias_por_numero[t.fecha.weekday()] == horario.dia
        and horario.horario_inicio <= t.hora < horario.horario_fin
        and t.estado != "Cancelado"
        for t in turnos_relacionados
    )
    if existe_turno_en_horario:
        raise ValueError("No se puede eliminar el horario porque tiene turnos activos asociados.")
    try:
        RepositorioHorario.eliminar(horario.id_horario)
        return True
    except IntegrityError as exc:
        raise ValueError("No se pudo eliminar el horario.") from exc

# Alias compatible con módulos de presentación de versiones anteriores.
listar_horario = listar_horarios
