from peewee import (
    Model, AutoField, CharField, TextField, IntegerField, BooleanField,
    TimeField, DateField, ForeignKeyField
)
from datos.conexion import database


class BaseModel(Model):
    class Meta:
        database = database


class Agenda(BaseModel):
    id_agenda = AutoField()
    jornada_laboral = CharField(max_length=100)

    class Meta:
        table_name = "agenda"


class Direccion(BaseModel):
    id_direccion = AutoField()
    calle = CharField(max_length=100)
    comuna = CharField(max_length=100)
    ciudad = CharField(max_length=100)
    numero_casa = IntegerField(null=True)

    class Meta:
        table_name = "direccion"


class Especialidad(BaseModel):
    id_especialidad = AutoField()
    nombre_especialidad = CharField(max_length=100)
    descripcion = TextField(null=True)

    class Meta:
        table_name = "especialidad"


class Usuario(BaseModel):
    id_usuario = AutoField()
    nombre = CharField(max_length=100)
    correo = CharField(max_length=100, unique=True)
    contrasena = CharField(max_length=225)

    class Meta:
        table_name = "usuario"


class Paciente(BaseModel):
    id_usuario = ForeignKeyField(
        Usuario, column_name="id_usuario", primary_key=True,
        backref="perfil_paciente", on_delete="CASCADE"
    )
    rut = CharField(max_length=20, unique=True)
    telefono = CharField(max_length=20, null=True)
    id_direccion = ForeignKeyField(
        Direccion, column_name="id_direccion", backref="pacientes",
        on_delete="RESTRICT"
    )

    class Meta:
        table_name = "pacientes"


class Medico(BaseModel):
    id_usuario = ForeignKeyField(
        Usuario, column_name="id_usuario", primary_key=True,
        backref="perfil_medico", on_delete="CASCADE"
    )
    numero_formacion = CharField(max_length=50, unique=True)
    id_especialidad = ForeignKeyField(
        Especialidad, column_name="id_especialidad", backref="medicos"
    )

    class Meta:
        table_name = "medico"

class Enfermero(BaseModel):
    id_usuario = ForeignKeyField(
        Usuario, column_name="id_usuario", primary_key=True, backref="enfermero"
    )
    rut = CharField(max_length=12, unique=True)
    telefono = CharField(max_length=20, null=True)
    area = CharField(max_length=80)

    class Meta:
        table_name = "enfermero"

class Horario(BaseModel):
    id_horario = AutoField()
    dia = CharField(max_length=20)
    horario_inicio = TimeField()
    horario_fin = TimeField()
    disponible = BooleanField(default=True)
    id_agenda = ForeignKeyField(
        Agenda, column_name="id_agenda", backref="horarios"
    )
    id_medico = ForeignKeyField(
        Medico, column_name="id_medico", backref="horarios"
    )

    class Meta:
        table_name = "horario"


class Turno(BaseModel):
    id_turno = AutoField()
    fecha = DateField()
    hora = TimeField()
    estado = CharField(max_length=20, default="Reservado")
    id_paciente = ForeignKeyField(
        Paciente, column_name="id_paciente", backref="turnos_paciente"
    )
    id_medico = ForeignKeyField(
        Medico, column_name="id_medico", backref="turnos_medico"
    )
    id_agenda = ForeignKeyField(
        Agenda, column_name="id_agenda", backref="turnos"
    )

    class Meta:
        table_name = "turno"
