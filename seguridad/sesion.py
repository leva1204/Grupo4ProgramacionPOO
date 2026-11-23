"""Gestión de la sesión autenticada y control de permisos."""
from functools import wraps

_usuario_actual = None

def iniciar_sesion(usuario):
    global _usuario_actual
    _usuario_actual = usuario

def cerrar_sesion():
    global _usuario_actual
    _usuario_actual = None

def obtener_usuario_actual():
    return _usuario_actual

def es_administrador():
    return bool(_usuario_actual and _usuario_actual.esadministrador)

def requiere_administrador(funcion):
    """Impide operaciones de escritura a usuarios sin privilegios."""
    @wraps(funcion)
    def protegida(*args, **kwargs):
        if not es_administrador():
            raise PermissionError("Acceso denegado: solo un administrador puede crear, modificar o eliminar datos.")
        return funcion(*args, **kwargs)
    return protegida
