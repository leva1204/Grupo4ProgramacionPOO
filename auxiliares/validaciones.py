import re
from datetime import datetime

def validar_rut(rut):
    patron_rut = r'^\d{1,3}(\.?\d{3})*-[0-9kK]$'
    if re.match(patron_rut, rut):
        rut_limpio = rut.replace('.', '').replace('-', '')
        digito_verificador = rut_limpio[-1]
        numero_rut = rut_limpio[:-1]
        rut_inverso = numero_rut[::-1]
        
        multiplicador = 2
        multiplicaciones = []
        
        for num in rut_inverso:
            mult = multiplicador * int(num)
            multiplicador += 1
            if multiplicador > 7:
                multiplicador = 2
            multiplicaciones.append(mult)
        
        total = sum(multiplicaciones)
        resto = total % 11
        digito_calculado = 11 - resto
        
        if digito_calculado == 11:
            digito_calculado = "0"
        elif digito_calculado == 10:
            digito_calculado = "K"
        else:
            digito_calculado = str(digito_calculado)
        
        return str(digito_verificador) == digito_calculado
    else:
        return False