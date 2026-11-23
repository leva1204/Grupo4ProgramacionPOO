# Medica In™

## Integrantes
- Luis Vargas
- Benjamin Cortes
- Damian Inostroza

## Descripcion
Medica In™, es un sistema que tiene como objetivo poder administrar, mediante funciones CRUD, la creacion, eliminacion, modificacion
y listado de turnos en un entorno medico, solo los usuarios de caracter administrativo tienen la habilidad de modificar datos
de la base de datos.

## Dependencias
Las dependencias necesarias para el funcionamiento del proyecto son las siguientes:
    peewee==4.5.3
    prettytable==3.18.0
    PyMySQL==1.2.3
    python-decouple==3.8
    wcwidth==0.9.2

## Procedimientos de instalacion

1. Instalar Python 3.10 o superior.
2. Instalar dependencias: `pip install -r requirements.txt`.
3. Configurar `.env` con las claves `db`, `host`, `port`, `user` y `password`.
4. Desde la carpeta raíz del proyecto, ejecutar `python app.py`.

## Procedimiento de creacion de base de datos
1. La base de datos se puede crear ejecutando el archivo `datos/sql/2026.09.08_12.10_DLL_MEDICAIN.sql` en MySQL.
2. Adicionalmente, puede llenar la base de datos de datos de caracter ejemplificativo, ejecutando el archivo `datos/sql/2026.22.11_19.42_insert_datos.sql`

## Usuario Inicial
Dentro de `datos/sql/2026.09.08_12.10_DLL_MEDICAIN.sql`, se puede encontrar un usuario administrador, con correo 
juanito.administrador.email.cl, y contraseña 'micontrasena', este usuario esta incorporado en el sistema con el fin de poder probar y debuggear sus mecanismos

## Organización por capas

- `presentacion/`: menús, captura de datos por consola y mensajes al usuario.
- `negocio/`: validaciones, reglas de negocio y coordinación de operaciones.
- `datos/repositorios/`: consultas, altas, modificaciones y eliminaciones mediante Peewee.
- `datos/modelos/models.py`: mapeo de tablas SQL a modelos.
- `datos/conexion.py`: conexión MySQL configurada desde `.env`.

### Instrucciones de ejecucion

- Al iniciar sesion se introducen las credencias del usuario, correo y contraseña, tiene 5 intentos para ingresar un correo valida que existe dentro del sistema, y una contraseña que este vinculada a dicho correo
- Una vez iniciada sesion, se puede acceder se pueden generar turnos medicos, estos dependen de la existencias de un paciente, un medico, 
un horario existente tomado por el medico y una agenda.
- **Cerrar sesión** termina la sesión actual y vuelve a solicitar credenciales; no cierra el programa.
- **Salir** cierra la aplicación.
- En **Gestión de Usuarios** se agregó **Cambiar perfil**, para asignar a otra cuenta el rol de Administrador o Usuario estándar.
- Por seguridad, una cuenta no puede cambiar su propio perfil mientras mantiene la sesión activa.
- El cambio de perfil está protegido en la capa de negocio y requiere una sesión de administrador.
