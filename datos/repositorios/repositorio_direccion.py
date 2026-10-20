from peewee import DoesNotExist, IntegrityError
from datos.modelos.models import Direccion

class RepositorioDireccion:
    @staticmethod
    def listar(): return list(Direccion.select().order_by(Direccion.ciudad, Direccion.comuna, Direccion.calle))
    
    @staticmethod
    def obtener(id_direccion):
        try: return Direccion.get(Direccion.id_direccion == int(id_direccion))
        except (DoesNotExist, ValueError, TypeError): return None

    @staticmethod
    def guardar(calle, comuna, ciudad, numero_casa=None):
        return Direccion.create(calle=calle, comuna=comuna, ciudad=ciudad, numero_casa=numero_casa)
    
    @staticmethod
    def actualizar(id_direccion, datos): return Direccion.update(**datos).where(Direccion.id_direccion == id_direccion).execute()
    
    @staticmethod
    def eliminar(id_direccion): return Direccion.delete().where(Direccion.id_direccion == id_direccion).execute()
