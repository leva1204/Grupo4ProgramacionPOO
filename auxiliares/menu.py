menu_superior = {
    '1': 'Gestión Turnos', '2': 'Gestión Pacientes', '3': 'Gestión Horarios',
    '4': 'Gestión Direcciones', '5': 'Gestión Especialidades', '6': 'Gestión Usuarios',
    '7': 'Gestión Médicos', '8': 'Gestión Agendas', '9': 'Salir'
}
def submenu(titulo, plural):
    return {'1': f'Crear {titulo}', '2': f'Listar {plural}', '3': f'Consultar {titulo}', '4': f'Modificar {titulo}', '5': f'Eliminar {titulo}', '6': 'Volver al menú anterior'}
menu_paciente = {'1':'Inscribir a un Paciente','2':'Listar todos los Pacientes','3':'Consultar un Paciente','4':'Modificar datos de un Paciente','5':'Eliminar un Paciente','6':'Volver al menú anterior'}
menu_horario = {'1':'Crear un Horario','2':'Listar todos los Horarios','3':'Consultar un Horario','4':'Modificar un Horario','5':'Eliminar un Horario','6':'Volver al menú anterior'}
menu_turno = {'1':'Generar un Turno','2':'Listar todos los Turnos','3':'Consultar un Turno','4':'Modificar datos de un Turno','5':'Eliminar un Turno','6':'Volver al menú anterior'}
menu_direccion = submenu('Dirección', 'Direcciones')
menu_especialidad = submenu('Especialidad', 'Especialidades')
menu_usuario = submenu('Usuario', 'Usuarios')
menu_medico = submenu('Médico', 'Médicos')
menu_agenda = submenu('Agenda', 'Agendas')
