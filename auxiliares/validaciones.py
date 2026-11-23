import re
from datetime import datetime

import re

patron_correo = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


def validar_correo(correo):
    if correo == "":
        return False, "No ingresaste ningún correo."

    if " " in correo:
        return False, "El correo no puede tener espacios."

    if "@" not in correo:
        return False, "Falta el '@' en el correo."

    if correo.count("@") > 1:
        return False, "El correo no puede tener más de un '@'."

    partes = correo.split("@")
    usuario = partes[0]
    dominio = partes[1]

    if usuario == "":
        return False, "Falta el nombre de usuario antes del '@'."

    errores_usuario = re.findall(r"[^a-zA-Z0-9._%+-]", usuario)
    if len(errores_usuario) > 0:
        return False, f"Usaste caracteres no permitidos antes del '@': {', '.join(errores_usuario)}"

    if usuario.startswith(".") or usuario.endswith("."):
        return False, "El usuario no puede empezar ni terminar con un punto."

    if ".." in usuario:
        return False, "No puedes poner dos puntos seguidos ('..')."

    if dominio == "":
        return False, "Falta el dominio después del '@' (ej: gmail.com)."

    errores_dominio = re.findall(r"[^a-zA-Z0-9.-]", dominio)
    if len(errores_dominio) > 0:
        return False, f"Usaste caracteres no permitidos en el dominio: {', '.join(errores_dominio)}"

    if "." not in dominio:
        return False, "Falta el punto y la extensión del dominio (ej: .cl o .com)."

    extension = dominio.split(".")[-1]
    if len(extension) < 2 or not extension.isalpha():
        return False, "La extensión después del punto debe tener al menos 2 letras (ej: .cl, .com)."

    if not re.match(patron_correo, correo):
        return False, "El formato del correo no es válido (debe ser usuario@dominio.com)."

    return True, "Correo válido"


def validar_rut(rut):
    rut = rut.strip().upper()

    # Solo permite 7 u 8 números, un guion y el dígito verificador (rechaza puntos y espacios)
    if not re.match(r"^\d{7,8}-[0-9K]$", rut):
        return False

    cuerpo, dv_ingresado = rut.split("-")

    suma = 0
    multiplo = 2
    for digito in reversed(cuerpo):
        suma += int(digito) * multiplo
        multiplo = 2 if multiplo == 7 else multiplo + 1

    resto = suma % 11
    dv_esperado = 11 - resto

    if dv_esperado == 11:
        dv_calculado = "0"
    elif dv_esperado == 10:
        dv_calculado = "K"
    else:
        dv_calculado = str(dv_esperado)

    return dv_ingresado == dv_calculado

def validar_contrasena(contrasena):
    """Valida la contraseña con el mínimo de 8 caracteres usado por el sistema."""
    if not contrasena:
        return False, "La contraseña es obligatoria."
    if len(contrasena) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres."
    return True, "Contraseña válida"
