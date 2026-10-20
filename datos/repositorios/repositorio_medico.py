from peewee import DoesNotExist
from datos.modelos.models import Medico

class RepositorioMedico:
    @staticmethod
    def listar(): return list(Medico.select().order_by(Medico.numero_formacion))

    @staticmethod
    def obtener(id_usuario):
        try: return Medico.get(Medico.id_usuario == int(id_usuario))
        except (DoesNotExist, ValueError, TypeError): return None

    @staticmethod
    def guardar(id_usuario, numero_formacion, id_especialidad):
        return Medico.create(id_usuario=id_usuario, numero_formacion=numero_formacion, id_especialidad=id_especialidad)
    
    @staticmethod
    def actualizar(id_usuario, datos): return Medico.update(**datos).where(Medico.id_usuario == id_usuario).execute()
    
    @staticmethod
    def eliminar(id_usuario): return Medico.delete().where(Medico.id_usuario == id_usuario).execute()
