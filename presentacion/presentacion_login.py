"""Pantalla de autenticación de Medica In."""
from getpass import getpass
from negocio.negocio_usuario import autenticar_usuario
from seguridad.sesion import iniciar_sesion

MAX_INTENTOS = 5

def solicitar_inicio_sesion():
    print("\n--- Inicio de sesión ---")
    for intento in range(1, MAX_INTENTOS + 1):
        correo = input("Correo electrónico: ").strip()
        contrasena = getpass("Contraseña: ")
        try:
            usuario = autenticar_usuario(correo, contrasena)
            if usuario is not None:
                iniciar_sesion(usuario)
                print(f"\nBienvenido/a, {usuario.nombre}.")
                return True
            print("Correo o contraseña incorrectos.")
        except ValueError as exc:
            print(f"Datos inválidos: {exc}")
        restantes = MAX_INTENTOS - intento
        if restantes:
            print(f"Intentos restantes: {restantes}\n")
    print("\nSe agotaron los 5 intentos. Acceso denegado.")
    return False
