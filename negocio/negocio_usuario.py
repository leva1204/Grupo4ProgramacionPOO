"""Reglas de negocio para cuentas generales de usuario.

Los datos personales exclusivos del paciente (RUT, teléfono y dirección) no
pertenecen a Usuario; se gestionan desde negocio_paciente.
"""


import hashlib
import hmac
from peewee import IntegrityError

from datos.modelos.models import Turno, Medico, Enfermero
from auxiliares.validaciones import validar_correo, validar_rut, validar_contrasena
from datos.repositorios.repositorio_usuario import RepositorioUsuario
from datos.repositorios.repositorio_medico import RepositorioMedico
from datos.repositorios.repositorio_enfermero import RepositorioEnfermero
from seguridad.sesion import requiere_administrador


TIPOS_USUARIO = {
    1: "Médico",
    2: "Enfermero/a"
}


def _hash_contrasena(contrasena):
    return hashlib.sha256(contrasena.encode("utf-8")).hexdigest()


def _correo(valor):
    valor = (valor or "").strip().lower()
    valido, mensaje = validar_correo(valor)
    if not valido:
        raise ValueError(mensaje)
    return valor


def _rut(valor):
    valor = (valor or "").strip().upper()
    if not validar_rut(valor):
        raise ValueError("RUT inválido. Ingréselo sin puntos y con guion (ej: 12345678-K).")
    return valor


def verificar_contrasena(contrasena_ingresada, contrasena_guardada):
    """Comprueba los formatos SHA-256 heredado y PBKDF2-SHA256 del sistema."""
    if not contrasena_ingresada or not contrasena_guardada:
        return False
    try:
        if contrasena_guardada.startswith("pbkdf2_sha256$"):
            algoritmo, iteraciones, sal_hex, hash_hex = contrasena_guardada.split("$", 3)
            if algoritmo != "pbkdf2_sha256":
                return False
            derivada = hashlib.pbkdf2_hmac(
                "sha256", contrasena_ingresada.encode("utf-8"),
                bytes.fromhex(sal_hex), int(iteraciones)
            ).hex()
            return hmac.compare_digest(derivada, hash_hex)
        hash_sha256 = hashlib.sha256(contrasena_ingresada.encode("utf-8")).hexdigest()
        return hmac.compare_digest(hash_sha256, contrasena_guardada)
    except (ValueError, TypeError):
        return False


def autenticar_usuario(correo, contrasena):
    correo = (correo or "").strip().lower()
    valido, mensaje = validar_correo(correo)
    if not valido:
        raise ValueError(mensaje)
    valido, mensaje = validar_contrasena(contrasena)
    if not valido:
        raise ValueError(mensaje)
    usuario = RepositorioUsuario.obtener_por_correo(correo)
    if usuario is None or not verificar_contrasena(contrasena, usuario.contrasena):
        return None
    return usuario


@requiere_administrador
def crear_usuario(nombre, correo, contrasena):
    nombre = (nombre or "").strip()
    if not nombre or len(nombre) > 100:
        raise ValueError("El nombre es obligatorio y debe tener hasta 100 caracteres.")
    correo = _correo(correo)
    valido, mensaje = validar_contrasena(contrasena)
    if not valido:
        raise ValueError(mensaje)
    if RepositorioUsuario.obtener_por_correo(correo):
        raise ValueError("Ese correo ya está registrado.")

    contrasena_hash = _hash_contrasena(contrasena)

    try:
        return RepositorioUsuario.guardar(nombre, correo, contrasena_hash)
    except IntegrityError as exc:
        raise ValueError("No se pudo crear el usuario; revise el correo.") from exc


def listar_usuarios():
    return RepositorioUsuario.listar()


def consultar_usuario(id_usuario):
    usuario = RepositorioUsuario.obtener(id_usuario)
    if usuario is None:
        raise ValueError("No se encontró el usuario.")
    return usuario


@requiere_administrador
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
        valido, mensaje = validar_contrasena(contrasena)
        if not valido:
            raise ValueError(mensaje)
        datos["contrasena"] = _hash_contrasena(contrasena)

    if not datos:
        raise ValueError("No se ingresaron cambios.")

    try:
        RepositorioUsuario.actualizar(usuario.id_usuario, datos)
    except IntegrityError as exc:
        raise ValueError("No se pudo actualizar el usuario.") from exc
    return consultar_usuario(usuario.id_usuario)


@requiere_administrador
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


@requiere_administrador
def cambiar_rol_usuario(id_usuario, esadministrador):
    """Cambia el perfil de acceso de una cuenta existente."""
    usuario = consultar_usuario(id_usuario)
    if not isinstance(esadministrador, bool):
        raise ValueError("El perfil indicado no es válido.")
    RepositorioUsuario.actualizar(
        usuario.id_usuario, {"esadministrador": esadministrador}
    )
    return consultar_usuario(usuario.id_usuario)


@requiere_administrador
def crear_medico(nombre, correo, contrasena, numero_formacion, id_especialidad):
    numero_formacion = str(numero_formacion).strip()
    if not numero_formacion:
        raise ValueError("El número de formación es obligatorio.")
    if any(m.numero_formacion == numero_formacion for m in RepositorioMedico.listar()):
        raise ValueError("Ese número de formación ya está registrado como médico.")

    usuario = crear_usuario(nombre, correo, contrasena)
    try:
        return RepositorioMedico.guardar(usuario.id_usuario, numero_formacion, id_especialidad)
    except IntegrityError as exc:
        RepositorioUsuario.eliminar(usuario.id_usuario)
        raise ValueError("No se pudo crear el médico; revise los datos o la especialidad.") from exc


@requiere_administrador
def crear_enfermero(nombre, correo, contrasena, rut, telefono, area):
    rut = _rut(rut)
    area = (area or "").strip()
    if not area:
        raise ValueError("El área de trabajo es obligatoria para el/la enfermero/a.")
    if RepositorioEnfermero.obtener_por_rut(rut):
        raise ValueError("Ese RUT ya está registrado como enfermero/a.")

    usuario = crear_usuario(nombre, correo, contrasena)
    try:
        return RepositorioEnfermero.guardar(usuario.id_usuario, rut, telefono, area)
    except IntegrityError as exc:
        RepositorioUsuario.eliminar(usuario.id_usuario)
        raise ValueError("No se pudo crear el/la enfermero/a; revise los datos.") from exc


def obtener_perfil_personal(id_usuario):
    """
    Devuelve (usuario, id_tipo, perfil) donde id_tipo es 1 (Médico) o 2 (Enfermero/a).
    """
    usuario = consultar_usuario(id_usuario)
    medico = RepositorioMedico.obtener(usuario.id_usuario)
    if medico:
        return usuario, 1, medico

    enfermero = RepositorioEnfermero.obtener(usuario.id_usuario)
    if enfermero:
        return usuario, 2, enfermero

    return usuario, None, None


def listar_personal(id_tipo=None):
    resultados = []
    for usuario in RepositorioUsuario.listar():
        _, tipo, perfil = obtener_perfil_personal(usuario.id_usuario)
        if tipo is None:
            continue
        if id_tipo is None or tipo == id_tipo:
            resultados.append((usuario, tipo, perfil))
    return resultados


@requiere_administrador
def actualizar_personal(id_usuario, nombre, correo, telefono, dato_extra):
    usuario, tipo, perfil = obtener_perfil_personal(id_usuario)
    if tipo is None:
        raise ValueError("El ID ingresado no corresponde a un médico ni a un/a enfermero/a.")

    actualizar_usuario(id_usuario, nombre=nombre, correo=correo)

    if tipo == 1:
        datos_perfil = {"id_especialidad": dato_extra}
        RepositorioMedico.actualizar(id_usuario, datos_perfil)
    elif tipo == 2:
        datos_perfil = {
            "telefono": telefono,
            "area": dato_extra,
        }
        RepositorioEnfermero.actualizar(id_usuario, datos_perfil)

@requiere_administrador
def eliminar_personal(id_usuario):
    usuario, tipo, perfil = obtener_perfil_personal(id_usuario)
    if tipo is None:
        raise ValueError("El ID ingresado no corresponde a un médico ni a un/a enfermero/a.")

    if tipo == 1:
        if Turno.select().where(Turno.id_medico == id_usuario).exists():
            raise ValueError("No se puede eliminar: el médico tiene turnos asociados.")
        RepositorioMedico.eliminar(id_usuario)
    elif tipo == 2:
        RepositorioEnfermero.eliminar(id_usuario)

    RepositorioUsuario.eliminar(id_usuario)
    return True