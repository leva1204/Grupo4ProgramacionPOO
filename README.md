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
4. Agregar informacion a las columnas de las tablas `datos/sql/2026.10.19_21.40_insert_informacion.sql`
5. Configurar `.env` con las claves `db`, `host`, `port`, `user` y `password`.
6. Desde la carpeta raíz del proyecto, ejecutar `python app.py`.

