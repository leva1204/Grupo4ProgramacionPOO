"""Reglas de negocio y validaciones de pacientes."""
import hashlib
import os
import re
from peewee import IntegrityError
from datos.modelos.models import Direccion, Usuario, Paciente, Turno
from datos.repositorios.repositorio_paciente import RepositorioPaciente


def _hash_contrasena(contrasena):
    sal = os.urandom(16)
    derivada = hashlib.pbkdf2_hmac("sha256", contrasena.encode("utf-8"), sal, 260_000)
    return f"pbkdf2_sha256$260000${sal.hex()}${derivada.hex()}"


def _validar_correo(correo):
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo or ""):
        raise ValueError("Ingrese un correo electrónico válido.")


def _validar_direccion(id_direccion):
    try:
        direccion = Direccion.get_or_none(Direccion.id_direccion == int(id_direccion))
    except (TypeError, ValueError):
        direccion = None
    if direccion is None:
        raise ValueError("Debe indicar una dirección existente para el paciente.")
    return direccion.id_direccion


def crear_paciente(nombre, correo, contrasena, rut, telefono=None, id_direccion=None):
    nombre = (nombre or "").strip()
    correo = (correo or "").strip().lower()
    rut = (rut or "").strip()
    if not nombre or len(nombre) > 100:
        raise ValueError("El nombre es obligatorio y no puede superar 100 caracteres.")
    _validar_correo(correo)
    if not contrasena or len(contrasena) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres.")
    if not rut or len(rut) > 20:
        raise ValueError("El RUT es obligatorio y no puede superar 20 caracteres.")
    if telefono and len(telefono.strip()) > 20:
        raise ValueError("El teléfono no puede superar 20 caracteres.")
    if RepositorioPaciente.obtener_por_correo(correo):
        raise ValueError("Ya existe un paciente con ese correo.")
    if RepositorioPaciente.obtener_por_rut(rut):
        raise ValueError("Ese RUT ya está registrado.")
    direccion = _validar_direccion(id_direccion)
    try:
        return RepositorioPaciente.guardar(
            nombre, correo, _hash_contrasena(contrasena), rut,
            (telefono or "").strip() or None, direccion
        )
    except IntegrityError as exc:
        raise ValueError("No se pudo registrar el paciente: revise correo, RUT y dirección.") from exc


def listar_pacientes():
    return RepositorioPaciente.listar()


def consultar_paciente(id_paciente):
    paciente = RepositorioPaciente.obtener(id_paciente)
    if paciente is None:
        raise ValueError("No se encontró el paciente.")
    return paciente


def actualizar_paciente(id_paciente, nombre=None, correo=None, rut=None,
                        telefono=None, id_direccion=None, contrasena=None):
    paciente = consultar_paciente(id_paciente)
    datos = {}
    usuario = paciente.id_usuario
    if nombre is not None:
        nombre = nombre.strip()
        if not nombre or len(nombre) > 100:
            raise ValueError("El nombre es obligatorio y no puede superar 100 caracteres.")
        datos["nombre"] = nombre
    if correo is not None:
        correo = correo.strip().lower()
        _validar_correo(correo)
        otro = Usuario.get_or_none((Usuario.correo == correo) &
                                   (Usuario.id_usuario != usuario.id_usuario))
        if otro:
            raise ValueError("Ese correo ya pertenece a otro usuario.")
        datos["correo"] = correo
    if rut is not None:
        rut = rut.strip()
        if not rut or len(rut) > 20:
            raise ValueError("El RUT es obligatorio y no puede superar 20 caracteres.")
        otro = Paciente.get_or_none((Paciente.rut == rut) &
                                    (Paciente.id_usuario != usuario.id_usuario))
        if otro:
            raise ValueError("Ese RUT ya pertenece a otro paciente.")
        datos["rut"] = rut
    if telefono is not None:
        telefono = telefono.strip() or None
        if telefono and len(telefono) > 20:
            raise ValueError("El teléfono no puede superar 20 caracteres.")
        datos["telefono"] = telefono
    if id_direccion is not None:
        datos["id_direccion"] = _validar_direccion(id_direccion)
    if contrasena:
        if len(contrasena) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")
        datos["contrasena"] = _hash_contrasena(contrasena)
    if not datos:
        raise ValueError("No se ingresaron campos para modificar.")
    try:
        RepositorioPaciente.actualizar(usuario.id_usuario, datos)
        return consultar_paciente(usuario.id_usuario)
    except IntegrityError as exc:
        raise ValueError("No se pudo actualizar el paciente por una restricción de datos.") from exc


def eliminar_paciente(id_paciente):
    paciente = consultar_paciente(id_paciente)
    if Turno.select().where(Turno.id_paciente == paciente.id_usuario_id).exists():
        raise ValueError("No se puede eliminar: el paciente tiene turnos asociados.")
    try:
        RepositorioPaciente.eliminar(paciente.id_usuario_id)
        return True
    except IntegrityError as exc:
        raise ValueError("No se puede eliminar: el paciente tiene registros relacionados.") from exc


listar_paciente = listar_pacientes
