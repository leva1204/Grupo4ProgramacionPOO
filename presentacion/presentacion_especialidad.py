from auxiliares.tablas import mostrar_tabla
from negocio.negocio_especialidad import crear_especialidad,listar_especialidades,consultar_especialidad,actualizar_especialidad,eliminar_especialidad

def _mostrar(especialidad): print(f'ID {especialidad.id_especialidad} | {especialidad.nombre_especialidad} | {especialidad.descripcion or "Sin descripción"}')
def solicitar_crear_especialidad():
    try:
        especialidad=crear_especialidad(input('Nombre de especialidad: '),input('Descripción (opcional): ')); print(f'Especialidad creada. ID: {especialidad.id_especialidad}')
    except Exception as error: print(f'No se pudo crear la especialidad: {error}')
def solicitar_listar_especialidad():
    try:
        especialidades = listar_especialidades()
        filas = [(especialidad_item.id_especialidad, especialidad_item.nombre_especialidad, especialidad_item.descripcion) for especialidad_item in especialidades]
        mostrar_tabla("Especialidades registradas", ["ID", "Especialidad", "Descripción"], filas, "No hay especialidades registradas.")
    except Exception as exc:
        print(f"No se pudieron listar las especialidades: {exc}")

def solicitar_consultar_especialidad():
    try: _mostrar(consultar_especialidad(input('ID especialidad: ').strip()))
    except Exception as error: print(f'No se pudo consultar la especialidad: {error}')
def solicitar_actualizar_especialidad():
    try:
        id_especialidad=input('ID especialidad: ').strip(); especialidad=consultar_especialidad(id_especialidad)
        nombre_especialidad=input(f'Nombre [{especialidad.nombre_especialidad}]: ').strip() or None; descripcion=input(f'Descripción [{especialidad.descripcion or "-"}]: ').strip() or None
        actualizar_especialidad(id_especialidad,nombre_especialidad,descripcion); print('Especialidad actualizada.')
    except Exception as error: print(f'No se pudo actualizar la especialidad: {error}')
def solicitar_eliminar_especialidad():
    try:
        id_especialidad=input('ID especialidad: ').strip(); especialidad=consultar_especialidad(id_especialidad)
        if input(f'¿Eliminar {especialidad.nombre_especialidad}? [s/N]: ').strip().lower()=='s': eliminar_especialidad(id_especialidad); print('Especialidad eliminada.')
        else: print('Operación cancelada.')
    except Exception as error: print(f'No se pudo eliminar la especialidad: {error}')
