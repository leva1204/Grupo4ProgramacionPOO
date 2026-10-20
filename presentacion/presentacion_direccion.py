from auxiliares.tablas import mostrar_tabla
from negocio.negocio_direccion import crear_direccion,listar_direcciones,consultar_direccion,actualizar_direccion,eliminar_direccion

def _mostrar(direccion): print(f"ID {direccion.id_direccion} | {direccion.calle} {direccion.numero_casa or ''}, {direccion.comuna}, {direccion.ciudad}")
def solicitar_crear_direccion():
    try:
        direccion=crear_direccion(input('Calle: '),input('Comuna: '),input('Ciudad: '),input('Número de casa (opcional): ').strip() or None); print(f'Dirección creada. ID: {direccion.id_direccion}')
    except Exception as error: print(f'No se pudo crear la dirección: {error}')
def solicitar_listar_direccion():
    try:
        direcciones = listar_direcciones()
        filas = [(direccion_item.id_direccion, direccion_item.calle, direccion_item.numero_casa, direccion_item.comuna, direccion_item.ciudad) for direccion_item in direcciones]
        mostrar_tabla("Direcciones registradas", ["ID", "Calle", "Número", "Comuna", "Ciudad"], filas, "No hay direcciones registradas.")
    except Exception as exc:
        print(f"No se pudieron listar las direcciones: {exc}")

def solicitar_consultar_direccion():
    try: _mostrar(consultar_direccion(input('ID dirección: ').strip()))
    except Exception as error: print(f'No se pudo consultar la dirección: {error}')
def solicitar_actualizar_direccion():
    try:
        id_direccion=input('ID dirección: ').strip(); direccion=consultar_direccion(id_direccion)
        calle=input(f'Calle [{direccion.calle}]: ').strip() or None; comuna=input(f'Comuna [{direccion.comuna}]: ').strip() or None; ciudad=input(f'Ciudad [{direccion.ciudad}]: ').strip() or None
        numero_casa=input(f'Número [{direccion.numero_casa or "-"}]: ').strip() or None
        actualizar_direccion(id_direccion,calle,comuna,ciudad,numero_casa); print('Dirección actualizada.')
    except Exception as error: print(f'No se pudo actualizar la dirección: {error}')
def solicitar_eliminar_direccion():
    try:
        id_direccion=input('ID dirección: ').strip(); direccion=consultar_direccion(id_direccion)
        if input(f'¿Eliminar dirección de {direccion.ciudad}? [s/N]: ').strip().lower()=='s': eliminar_direccion(id_direccion); print('Dirección eliminada.')
        else: print('Operación cancelada.')
    except Exception as error: print(f'No se pudo eliminar la dirección: {error}')
