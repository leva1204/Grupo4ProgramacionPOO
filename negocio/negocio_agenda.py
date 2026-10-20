from peewee import IntegrityError
from datos.modelos.models import Horario, Turno
from datos.repositorios.repositorio_agenda import RepositorioAgenda

def _jornada(valor):
    valor=(valor or '').strip()
    if not valor: raise ValueError('La jornada laboral es obligatoria.')
    if len(valor)>100: raise ValueError('La jornada laboral no puede superar 100 caracteres.')
    return valor

def crear_agenda(jornada_laboral):
    try: return RepositorioAgenda.guardar(_jornada(jornada_laboral))
    except IntegrityError as exc: raise ValueError('No se pudo crear la agenda.') from exc

def listar_agendas(): return RepositorioAgenda.listar()

def consultar_agenda(id_agenda):
    obj=RepositorioAgenda.obtener(id_agenda)
    if obj is None: raise ValueError('No se encontró la agenda.')
    return obj

def actualizar_agenda(id_agenda,jornada_laboral=None):
    obj=consultar_agenda(id_agenda)
    if jornada_laboral is None: raise ValueError('No se ingresaron cambios.')
    RepositorioAgenda.actualizar(obj.id_agenda,{'jornada_laboral':_jornada(jornada_laboral)})
    return consultar_agenda(obj.id_agenda)

def eliminar_agenda(id_agenda):
    obj=consultar_agenda(id_agenda)
    if Horario.select().where(Horario.id_agenda==obj.id_agenda).exists() or Turno.select().where(Turno.id_agenda==obj.id_agenda).exists(): raise ValueError('No se puede eliminar la agenda: tiene horarios o turnos asociados.')
    try: RepositorioAgenda.eliminar(obj.id_agenda); return True
    except IntegrityError as exc: raise ValueError('No se pudo eliminar la agenda.') from exc
