from auxiliares.tablas import mostrar_tabla
from negocio.negocio_agenda import crear_agenda,listar_agendas,consultar_agenda,actualizar_agenda,eliminar_agenda

def _mostrar(agenda): print(f'ID {agenda.id_agenda} | Jornada laboral: {agenda.jornada_laboral}')
def solicitar_crear_agenda():
    try:
        agenda=crear_agenda(input('Descripción de jornada laboral: ')); print(f'Agenda creada. ID: {agenda.id_agenda}')
    except Exception as error: print(f'No se pudo crear la agenda: {error}')
def solicitar_listar_agenda():
    try:
        agendas = listar_agendas()
        filas = [(agenda_item.id_agenda, agenda_item.jornada_laboral) for agenda_item in agendas]
        mostrar_tabla("Agendas registradas", ["ID", "Jornada laboral"], filas, "No hay agendas registradas.")
    except Exception as exc:
        print(f"No se pudieron listar las agendas: {exc}")

def solicitar_consultar_agenda():
    try: _mostrar(consultar_agenda(input('ID agenda: ').strip()))
    except Exception as error: print(f'No se pudo consultar la agenda: {error}')
def solicitar_actualizar_agenda():
    try:
        id_agenda=input('ID agenda: ').strip(); agenda=consultar_agenda(id_agenda); jornada_laboral=input(f'Jornada [{agenda.jornada_laboral}]: ').strip() or None
        actualizar_agenda(id_agenda,jornada_laboral); print('Agenda actualizada.')
    except Exception as error: print(f'No se pudo actualizar la agenda: {error}')
def solicitar_eliminar_agenda():
    try:
        id_agenda=input('ID agenda: ').strip(); agenda=consultar_agenda(id_agenda)
        if input(f'¿Eliminar agenda {agenda.jornada_laboral}? [s/N]: ').strip().lower()=='s': eliminar_agenda(id_agenda); print('Agenda eliminada.')
        else: print('Operación cancelada.')
    except Exception as error: print(f'No se pudo eliminar la agenda: {error}')
