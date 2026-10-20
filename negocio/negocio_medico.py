from peewee import IntegrityError
from datos.modelos.models import Usuario, Especialidad, Horario, Turno
from datos.repositorios.repositorio_medico import RepositorioMedico

def _refs(id_usuario,id_especialidad):
    try: u=Usuario.get_or_none(Usuario.id_usuario==int(id_usuario)); e=Especialidad.get_or_none(Especialidad.id_especialidad==int(id_especialidad))
    except (TypeError,ValueError): u=e=None
    if u is None: raise ValueError('Debe indicar un usuario existente para el médico.')
    if e is None: raise ValueError('La especialidad indicada no existe.')
    return u.id_usuario,e.id_especialidad

def crear_medico(id_usuario,numero_formacion,id_especialidad):
    numero_formacion=(numero_formacion or '').strip()
    if not numero_formacion or len(numero_formacion)>50: raise ValueError('El número de formación es obligatorio (máximo 50 caracteres).')
    uid,eid=_refs(id_usuario,id_especialidad)
    if RepositorioMedico.obtener(uid): raise ValueError('Ese usuario ya tiene un perfil médico.')
    if any(m.numero_formacion==numero_formacion for m in RepositorioMedico.listar()): raise ValueError('El número de formación ya está registrado.')
    try: return RepositorioMedico.guardar(uid,numero_formacion,eid)
    except IntegrityError as exc: raise ValueError('No se pudo registrar el médico; verifique las relaciones y el número de formación.') from exc

def listar_medicos(): return RepositorioMedico.listar()

def consultar_medico(id_usuario):
    obj=RepositorioMedico.obtener(id_usuario)
    if obj is None: raise ValueError('No se encontró el perfil médico.')
    return obj

def actualizar_medico(id_usuario,numero_formacion=None,id_especialidad=None):
    obj=consultar_medico(id_usuario); datos={}
    if numero_formacion is not None:
        numero_formacion=numero_formacion.strip()
        if not numero_formacion or len(numero_formacion)>50: raise ValueError('Número de formación inválido.')
        if any(m.id_usuario_id!=obj.id_usuario_id and m.numero_formacion==numero_formacion for m in RepositorioMedico.listar()): raise ValueError('El número de formación ya está registrado.')
        datos['numero_formacion']=numero_formacion
    if id_especialidad is not None:
        try: e=Especialidad.get_or_none(Especialidad.id_especialidad==int(id_especialidad))
        except (TypeError,ValueError): e=None
        if e is None: raise ValueError('La especialidad indicada no existe.')
        datos['id_especialidad']=e.id_especialidad
    if not datos: raise ValueError('No se ingresaron cambios.')
    try: RepositorioMedico.actualizar(obj.id_usuario_id,datos)
    except IntegrityError as exc: raise ValueError('No se pudo actualizar el médico.') from exc
    return consultar_medico(obj.id_usuario_id)

def eliminar_medico(id_usuario):
    obj=consultar_medico(id_usuario)
    if Horario.select().where(Horario.id_medico==obj.id_usuario_id).exists() or Turno.select().where(Turno.id_medico==obj.id_usuario_id).exists(): raise ValueError('No se puede eliminar el médico: tiene horarios o turnos asociados.')
    try: RepositorioMedico.eliminar(obj.id_usuario_id); return True
    except IntegrityError as exc: raise ValueError('No se pudo eliminar el médico.') from exc
