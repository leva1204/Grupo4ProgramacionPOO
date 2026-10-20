from peewee import IntegrityError
from datos.modelos.models import Usuario
from datos.repositorios.repositorio_direccion import RepositorioDireccion

def _texto(valor, campo, maximo=100):
    valor=(valor or '').strip()
    if not valor: raise ValueError(f'{campo} es obligatorio.')
    if len(valor)>maximo: raise ValueError(f'{campo} no puede superar {maximo} caracteres.')
    return valor

def _numero_casa(valor):
    if valor in (None, ''): return None
    try: n=int(valor)
    except (TypeError,ValueError): raise ValueError('El número de casa debe ser un entero.')
    if n<0: raise ValueError('El número de casa no puede ser negativo.')
    return n

def crear_direccion(calle, comuna, ciudad, numero_casa=None):
    try: return RepositorioDireccion.guardar(_texto(calle,'La calle'),_texto(comuna,'La comuna'),_texto(ciudad,'La ciudad'),_numero_casa(numero_casa))
    except IntegrityError as exc: raise ValueError('No se pudo crear la dirección.') from exc

def listar_direcciones(): return RepositorioDireccion.listar()
def consultar_direccion(id_direccion):
    obj=RepositorioDireccion.obtener(id_direccion)
    if obj is None: raise ValueError('No se encontró la dirección.')
    return obj

def actualizar_direccion(id_direccion, calle=None, comuna=None, ciudad=None, numero_casa=None):
    obj=consultar_direccion(id_direccion); datos={}
    for campo,valor in [('calle',calle),('comuna',comuna),('ciudad',ciudad)]:
        if valor is not None: datos[campo]=_texto(valor,campo.replace('_',' ').capitalize())
    if numero_casa is not None: datos['numero_casa']=_numero_casa(numero_casa)
    if not datos: raise ValueError('No se ingresaron cambios.')
    try: RepositorioDireccion.actualizar(obj.id_direccion,datos)
    except IntegrityError as exc: raise ValueError('No se pudo actualizar la dirección.') from exc
    return consultar_direccion(obj.id_direccion)

def eliminar_direccion(id_direccion):
    obj=consultar_direccion(id_direccion)
    if Usuario.select().where(Usuario.id_direccion==obj.id_direccion).exists(): raise ValueError('No se puede eliminar: hay usuarios asociados a esta dirección.')
    try: RepositorioDireccion.eliminar(obj.id_direccion); return True
    except IntegrityError as exc: raise ValueError('No se pudo eliminar la dirección.') from exc
