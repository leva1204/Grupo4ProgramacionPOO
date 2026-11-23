from datos.modelos.models import Enfermero


class RepositorioEnfermero:
    @staticmethod
    def guardar(id_usuario, rut, telefono, area):
        return Enfermero.create(
            id_usuario=id_usuario,
            rut=rut,
            telefono=telefono,
            area=area,
        )

    @staticmethod
    def listar():
        return list(Enfermero.select())

    @staticmethod
    def obtener(id_usuario):
        return Enfermero.get_or_none(Enfermero.id_usuario == id_usuario)

    @staticmethod
    def obtener_por_rut(rut):
        return Enfermero.get_or_none(Enfermero.rut == rut)

    @staticmethod
    def actualizar(id_usuario, datos):
        Enfermero.update(**datos).where(Enfermero.id_usuario == id_usuario).execute()

    @staticmethod
    def eliminar(id_usuario):
        Enfermero.delete().where(Enfermero.id_usuario == id_usuario).execute()