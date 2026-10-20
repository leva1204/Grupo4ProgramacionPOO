from peewee import IntegrityError
from datos.modelos.models import Medico
from datos.repositorios.repositorio_especialidad import RepositorioEspecialidad

def _nombre(valor):
    valor=(valor or '').strip()
    if not valor: raise ValueError('El nombre de la especialidad es obligatorio.')
    if len(valor)>100: raise ValueError('El nombre no puede superar 100 caracteres.')
    return valor

def crear_especialidad(nombre_especialidad, descripcion=None):
    descripcion=(descripcion or '').strip() or None
    try: return RepositorioEspecialidad.guardar(_nombre(nombre_especialidad),descripcion)
    except IntegrityError as exc: raise ValueError('No se pudo crear la especialidad.') from exc

def listar_especialidades(): return RepositorioEspecialidad.listar()

def consultar_especialidad(id_especialidad):
    obj=RepositorioEspecialidad.obtener(id_especialidad)
    if obj is None: raise ValueError('No se encontró la especialidad.')
    return obj

def actualizar_especialidad(id_especialidad,nombre_especialidad=None,descripcion=None):
    obj=consultar_especialidad(id_especialidad); datos={}
    if nombre_especialidad is not None: datos['nombre_especialidad']=_nombre(nombre_especialidad)
    if descripcion is not None: datos['descripcion']=descripcion.strip() or None
    if not datos: raise ValueError('No se ingresaron cambios.')
    RepositorioEspecialidad.actualizar(obj.id_especialidad,datos)
    return consultar_especialidad(obj.id_especialidad)

def eliminar_especialidad(id_especialidad):
    obj=consultar_especialidad(id_especialidad)
    if Medico.select().where(Medico.id_especialidad==obj.id_especialidad).exists(): raise ValueError('No se puede eliminar: existen médicos con esta especialidad.')
    try: RepositorioEspecialidad.eliminar(obj.id_especialidad); return True
    except IntegrityError as exc: raise ValueError('No se pudo eliminar la especialidad.') from exc
