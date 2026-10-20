from prettytable import PrettyTable


def mostrar_tabla(titulo, columnas, filas, mensaje_vacio="No hay registros."):
    print(f"\n--- {titulo} ---")
    if not filas:
        print(mensaje_vacio)
        return
    tabla = PrettyTable()
    tabla.field_names = columnas
    tabla.align = "l"
    for fila in filas:
        tabla.add_row(["-" if valor is None or valor == "" else valor for valor in fila])
    print(tabla)
