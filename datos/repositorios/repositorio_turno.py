from peewee import DoesNotExist
from datos.modelos.models import Turno


class RepositorioTurno:
    @staticmethod
    def listar():
        return list(Turno.select().order_by(Turno.fecha, Turno.hora))

    @staticmethod
    def obtener(id_turno):
        try:
            return Turno.get(Turno.id_turno == id_turno)
        except (DoesNotExist, ValueError, TypeError):
            return None

    @staticmethod
    def guardar(fecha, hora, estado, id_paciente, id_medico, id_agenda):
        return Turno.create(
            fecha=fecha, hora=hora, estado=estado,
            id_paciente=id_paciente, id_medico=id_medico, id_agenda=id_agenda
        )

    @staticmethod
    def actualizar(id_turno, datos):
        return (Turno.update(**datos)
                .where(Turno.id_turno == id_turno).execute())

    @staticmethod
    def eliminar(id_turno):
        return (Turno.delete()
                .where(Turno.id_turno == id_turno).execute())

    @staticmethod
    def existe_reserva(fecha, hora, id_medico, excluir=None):
        consulta = Turno.select().where(
            (Turno.fecha == fecha) &
            (Turno.hora == hora) &
            (Turno.id_medico == id_medico) &
            (Turno.estado != "Cancelado")
        )
        if excluir is not None:
            consulta = consulta.where(Turno.id_turno != excluir)
        return consulta.exists()

    @staticmethod
    def listar_por_paciente(id_paciente):
        return list(Turno.select().where(
            Turno.id_paciente == id_paciente
        ).order_by(Turno.fecha, Turno.hora))
