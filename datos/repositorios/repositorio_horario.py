from peewee import DoesNotExist
from datos.modelos.models import Horario


class RepositorioHorario:
    @staticmethod
    def listar():
        return list(Horario.select().order_by(Horario.dia, Horario.horario_inicio))

    @staticmethod
    def obtener(id_horario):
        try:
            return Horario.get(Horario.id_horario == id_horario)
        except (DoesNotExist, ValueError, TypeError):
            return None

    @staticmethod
    def guardar(dia, horario_inicio, horario_fin, disponible, id_agenda, id_medico):
        return Horario.create(
            dia=dia, horario_inicio=horario_inicio, horario_fin=horario_fin,
            disponible=disponible, id_agenda=id_agenda, id_medico=id_medico
        )

    @staticmethod
    def actualizar(id_horario, datos):
        return (Horario.update(**datos)
                .where(Horario.id_horario == id_horario).execute())

    @staticmethod
    def eliminar(id_horario):
        return (Horario.delete()
                .where(Horario.id_horario == id_horario).execute())

    @staticmethod
    def buscar_solapamiento(dia, inicio, fin, id_medico, id_agenda, excluir=None):
        consulta = Horario.select().where(
            (Horario.dia == dia) &
            (Horario.id_medico == id_medico) &
            (Horario.id_agenda == id_agenda) &
            (Horario.horario_inicio < fin) &
            (Horario.horario_fin > inicio)
        )
        if excluir is not None:
            consulta = consulta.where(Horario.id_horario != excluir)
        return consulta.exists()
