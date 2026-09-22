
DROP DATABASE if EXISTS turnomed;
CREATE DATABASE turnomed;
CREATE TABLE Paciente (
    id_usuario INT PRIMARY KEY,
    rut VARCHAR(20) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    id_direccion INT NOT NULL,
    CONSTRAINT fk_paciente_usuario FOREING KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
    CONSTRAINT fk_paciente_direccion FOREING KEY (id_direccion) REFERENCES Direccion(id_direccion)
);
