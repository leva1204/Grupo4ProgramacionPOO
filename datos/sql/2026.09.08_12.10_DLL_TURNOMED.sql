
DROP DATABASE if EXISTS turnomed;
CREATE DATABASE turnomed;

CREATE TABLE cargo(
    id_tipo_direccion INTEGER AUTO_INCREMENT,
    nombre VARCHAR (25) NOT NULL,
    descripcion: VARCHAR(255) NULL,
)