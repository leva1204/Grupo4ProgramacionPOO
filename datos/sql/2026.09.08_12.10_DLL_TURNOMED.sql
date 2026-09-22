
DROP DATABASE if EXISTS turnomed;
CREATE DATABASE turnomed;

USE turnomed

CREATE TABLE Direccion(
    id_direccion INT AUTO_INCREMENT PRIMARY KEY,
    calle VARCHAR(100) NOT NULL,
    comuna VARCHAR(100) NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    numero_casa INT
);

CREATE TABLE Especialidad(
    id_especialidad INT AUTO_INCREMENT PRIMARY KEY,
    nombre_especialidad VARCHAR(100) NOT NULL,
    descripcion TEXT
);

CREATE TABLE Usuario(
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(225) NOT NULL
    rut VARCHAR(20) UNIQUE,
    telefono VARCHAR(20),
    id_direccion INT
    CONSTRAINT fk_usuario_direccion FOREIGN KEY (id_direccion) REFERENCES Direccion(id_direccion)
);

CREATE TABLE Medico(
    id_usuario INT PRIMARY KEY,
    numero_formacion VARCHAR(50) NOT NULL UNIQUE,
    id_especialidad INT NOT NULL,
    CONSTRAINT fk_medico_usuario FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
    CONSTRAINT fk_medico_especialidad FOREIGN KEY (id_especialidad) REFERENCES Especialidad(id_especialidad)
);

CREATE TABLE Agenda(
    id_agenda INT AUTO_INCREMENT PRIMARY KEY,
    jornada_laboral VARCHAR(100) NOT NULL
);

CREATE TABLE Horario(
    id_horario INT AUTO_INCREMENT PRIMARY KEY,
    dia VARCHAR(20) NOT NULL,
    horario_inicio TIME NOT NULL,
    horario_fin TIME NOT NULL,
    disponible BOOLEAN DEFAULT TRUE,
    id_agenda INT NOT NULL,
    id_medico INT NOT NULL,
    CONSTRAINT fk_horario_agenda FOREIGN KEY (id_agenda) REFERENCES Agenda(id_agenda),
    CONSTRAINT fk_horario_medico FOREIGN KEY (id_medico) REFERENCES Medico(id_usuario)
);

CREATE TABLE Turno(
    id_turno INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado ENUM('Reservado', 'Confirmado', 'Atendido', 'Cancelado') NOT NULL DEFAULT 'Reservado',
    id_paciente INT NOT NULL,
    id_medico INT NOT NULL,
    id_agenda INT NOT NULL,
    CONSTRAINT fk_turno_paciente FOREIGN KEY (id_paciente) REFERENCES Usuario(id_usuario),
    CONSTRAINT fk_turno_medico FOREIGN KEY (id_medico) REFERENCES Medico(id_usuario),
    CONSTRAINT fk_turno_agenda FOREIGN KEY (id_agenda) REFERENCES Agenda(id_agenda)
);