from peewee import DoesNotExist
from datos.modelos.models import Usuario


class RepositorioUsuario:
    @staticmethod
    def listar():
        return list(Usuario.select().order_by(Usuario.nombre))

    @staticmethod
    def obtener(id_usuario):
        try:
            return Usuario.get(Usuario.id_usuario == int(id_usuario))
        except (DoesNotExist, ValueError, TypeError):
            return None

    @staticmethod
    def obtener_por_correo(correo):
        try:
            return Usuario.get(Usuario.correo == correo)
        except DoesNotExist:
            return None

    @staticmethod
    def guardar(nombre, correo, contrasena):
        return Usuario.create(nombre=nombre, correo=correo, contrasena=contrasena)

    @staticmethod
    def actualizar(id_usuario, datos):
        return Usuario.update(**datos).where(
            Usuario.id_usuario == int(id_usuario)
        ).execute()

    @staticmethod
    def eliminar(id_usuario):
        return Usuario.delete().where(
            Usuario.id_usuario == int(id_usuario)
        ).execute()
