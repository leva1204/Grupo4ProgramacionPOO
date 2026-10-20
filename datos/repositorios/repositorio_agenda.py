from peewee import DoesNotExist
from datos.modelos.models import Agenda

class RepositorioAgenda:
    @staticmethod
    def listar(): return list(Agenda.select().order_by(Agenda.jornada_laboral))

    @staticmethod
    def obtener(id_agenda):
        try: return Agenda.get(Agenda.id_agenda == int(id_agenda))
        except (DoesNotExist, ValueError, TypeError): return None

    @staticmethod
    def guardar(jornada_laboral): return Agenda.create(jornada_laboral=jornada_laboral)

    @staticmethod
    def actualizar(id_agenda, datos): return Agenda.update(**datos).where(Agenda.id_agenda == id_agenda).execute()
    
    @staticmethod
    def eliminar(id_agenda): return Agenda.delete().where(Agenda.id_agenda == id_agenda).execute()
