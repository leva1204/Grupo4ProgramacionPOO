from peewee import DoesNotExist
from datos.modelos.models import Especialidad

class RepositorioEspecialidad:
    @staticmethod
    def listar(): return list(Especialidad.select().order_by(Especialidad.nombre_especialidad))

    @staticmethod
    def obtener(id_especialidad):
        try: return Especialidad.get(Especialidad.id_especialidad == int(id_especialidad))
        except (DoesNotExist, ValueError, TypeError): return None

    @staticmethod
    def guardar(nombre_especialidad, descripcion=None):
        return Especialidad.create(nombre_especialidad=nombre_especialidad, descripcion=descripcion)
    
    @staticmethod
    def actualizar(id_especialidad, datos): return Especialidad.update(**datos).where(Especialidad.id_especialidad == id_especialidad).execute()
    
    @staticmethod
    def eliminar(id_especialidad): return Especialidad.delete().where(Especialidad.id_especialidad == id_especialidad).execute()
