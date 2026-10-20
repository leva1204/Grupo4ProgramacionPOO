"""Acceso a datos para la tabla Pacientes y su Usuario asociado."""
from peewee import DoesNotExist
from datos.modelos.models import Usuario, Paciente


class RepositorioPaciente:
    @staticmethod
    def listar():
        return list(
            Paciente.select(Paciente, Usuario)
            .join(Usuario)
            .order_by(Usuario.nombre)
        )

    @staticmethod
    def obtener(id_paciente):
        try:
            return (Paciente.select(Paciente, Usuario)
                    .join(Usuario)
                    .where(Paciente.id_usuario == int(id_paciente))
                    .get())
        except (DoesNotExist, ValueError, TypeError):
            return None

    @staticmethod
    def obtener_por_correo(correo):
        try:
            return (Paciente.select(Paciente, Usuario)
                    .join(Usuario)
                    .where(Usuario.correo == correo)
                    .get())
        except DoesNotExist:
            return None

    @staticmethod
    def obtener_por_rut(rut):
        try:
            return Paciente.get(Paciente.rut == rut)
        except DoesNotExist:
            return None

    @staticmethod
    def guardar(nombre, correo, contrasena, rut, telefono=None, id_direccion=None):
        with Usuario._meta.database.atomic():
            usuario = Usuario.create(
                nombre=nombre, correo=correo, contrasena=contrasena
            )
            Paciente.create(
                id_usuario=usuario.id_usuario,
                rut=rut,
                telefono=telefono or None,
                id_direccion=id_direccion
            )
        return RepositorioPaciente.obtener(usuario.id_usuario)

    @staticmethod
    def actualizar(id_paciente, datos):
        id_paciente = int(id_paciente)
        datos_usuario = {k: v for k, v in datos.items()
                         if k in {"nombre", "correo", "contrasena"}}
        datos_paciente = {k: v for k, v in datos.items()
                          if k in {"rut", "telefono", "id_direccion"}}
        db = Usuario._meta.database
        with db.atomic():
            if datos_usuario:
                Usuario.update(**datos_usuario).where(
                    Usuario.id_usuario == id_paciente
                ).execute()
            if datos_paciente:
                Paciente.update(**datos_paciente).where(
                    Paciente.id_usuario == id_paciente
                ).execute()
        return RepositorioPaciente.obtener(id_paciente)

    @staticmethod
    def eliminar(id_paciente):
        # El borrado del usuario elimina su registro Pacientes por ON DELETE CASCADE.
        return Usuario.delete().where(
            Usuario.id_usuario == int(id_paciente)
        ).execute()
