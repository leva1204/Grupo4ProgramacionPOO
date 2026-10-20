# Medica In™ — módulos CRUD de horarios, turnos y pacientes

## Organización por capas

- `presentacion/`: menús, captura de datos por consola y mensajes al usuario.
- `negocio/`: validaciones, reglas de negocio y coordinación de operaciones.
- `datos/repositorios/`: consultas, altas, modificaciones y eliminaciones mediante Peewee.
- `datos/modelos/models.py`: mapeo de tablas SQL a modelos.
- `datos/conexion.py`: conexión MySQL configurada desde `.env`.

## Requisitos y ejecución

1. Instalar Python 3.10 o superior.
2. Instalar dependencias: `pip install -r requirements.txt`.
3. Crear la base de datos ejecutando `datos/sql/2026.09.08_12.10_DLL_TURNOMED.sql` en MySQL.
4. Configurar `.env` con las claves `db`, `host`, `port`, `user` y `password`.
5. Desde la carpeta raíz del proyecto, ejecutar `python app.py`.

No ejecutar el DDL principal en una base con datos que se quieran conservar: contiene `DROP DATABASE`.

## Importante sobre Paciente

El DDL principal del proyecto no crea una tabla `Paciente`. La tabla `Turno` referencia `Usuario.id_usuario` como `id_paciente`, por lo que este CRUD registra y administra pacientes como filas de `usuario`. El archivo `2026.21.09_12.20_DLL_TURNOMED.sql` intenta crear una tabla `Paciente` independiente, pero contiene errores de sintaxis y no es compatible con la relación definida en el DDL principal. Para evitar inconsistencias, este código conserva el esquema principal.

La contraseña ingresada para un paciente se almacena con hash PBKDF2-HMAC-SHA256, no en texto plano. Si el proyecto ya tiene un módulo de autenticación, debe usar el mismo formato de hash.

## Reglas implementadas

- Paciente: campos obligatorios, formato de correo, longitud mínima de contraseña, unicidad de correo y RUT y validación de dirección.
- Horario: día válido, hora inicial anterior a la final, existencia de médico y agenda y prevención de solapamientos por médico/agenda.
- Turno: fecha no pasada, referencias válidas, coincidencia con horario disponible, prevención de reservas duplicadas y transición controlada de estados.
- Los borrados pueden rechazarse cuando las claves foráneas o el historial de turnos impidan la operación.

## Nota

La implementación está basada en los archivos incluidos en el ZIP y requiere probarse contra una instancia MySQL real con el esquema cargado. No se incluyen credenciales reales.


## CRUD por capas para todas las tablas

Se añadieron módulos `repositorio`, `negocio` y `presentacion` para Direccion, Especialidad, Usuario, Medico y Agenda, además de los módulos existentes para Horario, Turno y Paciente. Los menús de consola ahora permiten acceder a estos CRUD.

**Nota sobre el modelo de datos:** el DDL principal no define una tabla `Paciente` independiente; `Turno.id_paciente` referencia `Usuario.id_usuario`. Por eso Paciente y Usuario administran registros de la misma tabla `usuario`. Medico es un perfil relacionado con un Usuario existente y usa `id_usuario` como clave primaria.

Para ejecutar, instala las dependencias de `requirements.txt`, configura `.env` y ejecuta `python app.py` desde la carpeta raíz.
