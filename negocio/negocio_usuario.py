"""Reglas de negocio para cuentas generales de usuario.

Los datos personales exclusivos del paciente (RUT, teléfono y dirección) no
pertenecen a Usuario; se gestionan desde negocio_paciente.
"""
import re

from peewee import IntegrityError

from datos.modelos.models import Turno
from datos.repositorios.repositorio_usuario import RepositorioUsuario


def _correo(valor):
    valor = (valor or "").strip().lower()
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor):
        raise ValueError("Ingrese un correo válido.")
    return valor


def crear_usuario(nombre, correo, contrasena):
    nombre = (nombre or "").strip()
    if not nombre or len(nombre) > 100:
        raise ValueError("El nombre es obligatorio y debe tener hasta 100 caracteres.")
    correo = _correo(correo)
    if not contrasena or len(contrasena) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres.")
    if RepositorioUsuario.obtener_por_correo(correo):
        raise ValueError("Ese correo ya está registrado.")
    try:
        return RepositorioUsuario.guardar(nombre, correo, contrasena)
    except IntegrityError as exc:
        raise ValueError("No se pudo crear el usuario; revise el correo.") from exc


def listar_usuarios():
    return RepositorioUsuario.listar()


def consultar_usuario(id_usuario):
    usuario = RepositorioUsuario.obtener(id_usuario)
    if usuario is None:
        raise ValueError("No se encontró el usuario.")
    return usuario


def actualizar_usuario(id_usuario, nombre=None, correo=None, contrasena=None):
    usuario = consultar_usuario(id_usuario)
    datos = {}

    if nombre is not None:
        nombre = nombre.strip()
        if not nombre or len(nombre) > 100:
            raise ValueError("El nombre es obligatorio y debe tener hasta 100 caracteres.")
        datos["nombre"] = nombre

    if correo is not None:
        correo = _correo(correo)
        otro = RepositorioUsuario.obtener_por_correo(correo)
        if otro and otro.id_usuario != usuario.id_usuario:
            raise ValueError("Ese correo ya está registrado.")
        datos["correo"] = correo

    if contrasena:
        if len(contrasena) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")
        datos["contrasena"] = contrasena

    if not datos:
        raise ValueError("No se ingresaron cambios.")

    try:
        RepositorioUsuario.actualizar(usuario.id_usuario, datos)
    except IntegrityError as exc:
        raise ValueError("No se pudo actualizar el usuario.") from exc
    return consultar_usuario(usuario.id_usuario)


def eliminar_usuario(id_usuario):
    usuario = consultar_usuario(id_usuario)
    if Turno.select().where(Turno.id_paciente == usuario.id_usuario).exists():
        raise ValueError("No se puede eliminar: el usuario tiene turnos asociados.")
    try:
        RepositorioUsuario.eliminar(usuario.id_usuario)
        return True
    except IntegrityError as exc:
        raise ValueError(
            "No se pudo eliminar el usuario; puede tener relaciones activas."
        ) from exc
