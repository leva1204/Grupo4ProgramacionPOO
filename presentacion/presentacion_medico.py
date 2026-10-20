from auxiliares.tablas import mostrar_tabla
from negocio.negocio_medico import crear_medico,listar_medicos,consultar_medico,actualizar_medico,eliminar_medico

def _mostrar(medico): print(f'Usuario ID {medico.id_usuario_id} | {medico.id_usuario.nombre} | Formación: {medico.numero_formacion} | Especialidad ID: {medico.id_especialidad_id} ({medico.id_especialidad.nombre_especialidad})')
def solicitar_crear_medico():
    try:
        medico=crear_medico(input('ID usuario existente: ').strip(),input('Número de formación: ').strip(),input('ID especialidad: ').strip()); print(f'Perfil médico creado para usuario {medico.id_usuario_id}.')
    except Exception as error: print(f'No se pudo crear el médico: {error}')
def solicitar_listar_medico():
    try:
        medicos = listar_medicos()
        filas = [(medico_item.id_usuario_id, medico_item.id_usuario.nombre, medico_item.numero_formacion,
                  medico_item.id_especialidad_id, medico_item.id_especialidad.nombre_especialidad) for medico_item in medicos]
        mostrar_tabla("Médicos registrados", ["ID usuario", "Nombre", "N.º formación", "ID especialidad", "Especialidad"], filas, "No hay médicos registrados.")
    except Exception as exc:
        print(f"No se pudieron listar los médicos: {exc}")

def solicitar_consultar_medico():
    try: _mostrar(consultar_medico(input('ID usuario del médico: ').strip()))
    except Exception as error: print(f'No se pudo consultar el médico: {error}')
def solicitar_actualizar_medico():
    try:
        id_usuario=input('ID usuario del médico: ').strip(); medico=consultar_medico(id_usuario)
        numero_formacion=input(f'Número de formación [{medico.numero_formacion}]: ').strip() or None; id_especialidad=input(f'ID especialidad [{medico.id_especialidad_id}]: ').strip() or None
        actualizar_medico(id_usuario,numero_formacion,id_especialidad); print('Médico actualizado.')
    except Exception as error: print(f'No se pudo actualizar el médico: {error}')
def solicitar_eliminar_medico():
    try:
        id_usuario=input('ID usuario del médico: ').strip(); medico=consultar_medico(id_usuario)
        if input(f'¿Eliminar perfil médico de {medico.id_usuario.nombre}? [s/N]: ').strip().lower()=='s': eliminar_medico(id_usuario); print('Perfil médico eliminado; el usuario permanece registrado.')
        else: print('Operación cancelada.')
    except Exception as error: print(f'No se pudo eliminar el médico: {error}')
