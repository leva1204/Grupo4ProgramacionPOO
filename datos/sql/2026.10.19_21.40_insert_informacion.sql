-- 1. Direccion
INSERT INTO Direccion (id_direccion, calle, comuna, ciudad, numero_casa) VALUES
(1, 'Av. Alemania', 'Temuco', 'Temuco', 101),
(2, 'Calle Prat', 'Temuco', 'Temuco', 202),
(3, 'Av. Pablo Neruda', 'Temuco', 'Temuco', 303),
(4, 'Calle Manuel Montt', 'Padre Las Casas', 'Temuco', 404),
(5, 'Av. Caupolican', 'Temuco', 'Temuco', 505),
(6, 'Calle Bulnes', 'Villarrica', 'Villarrica', 606),
(7, 'Av. Los Poetas', 'Temuco', 'Temuco', 707),
(8, 'Calle O Higgins', 'Nueva Imperial', 'Nueva Imperial', 808),
(9, 'Av. Recabarren', 'Temuco', 'Temuco', 909),
(10, 'Calle Portales', 'Lautaro', 'Lautaro', 1001);

-- 2. Especialidad
INSERT INTO Especialidad (id_especialidad, nombre_especialidad, descripcion) VALUES
(1, 'Medicina General', 'Atencion medica general'),
(2, 'Cardiologia', 'Diagnostico y tratamiento cardiovascular'),
(3, 'Dermatologia', 'Atencion de enfermedades de la piel'),
(4, 'Pediatria', 'Atencion medica infantil'),
(5, 'Neurologia', 'Atencion del sistema nervioso'),
(6, 'Traumatologia', 'Lesiones del sistema musculoesqueletico'),
(7, 'Oftalmologia', 'Atencion de la salud visual'),
(8, 'Ginecologia', 'Salud reproductiva femenina'),
(9, 'Psiquiatria', 'Atencion de la salud mental'),
(10, 'Endocrinologia', 'Enfermedades hormonales y metabolicas');

-- 3. Usuario
INSERT INTO Usuario (id_usuario, nombre, correo, contrasena) VALUES
(1, 'Dra. Ana Perez', 'ana.perez@example.com', 'clave_demo_01'),
(2, 'Dr. Carlos Soto', 'carlos.soto@example.com', 'clave_demo_02'),
(3, 'Dra. Maria Gonzalez', 'maria.gonzalez@example.com', 'clave_demo_03'),
(4, 'Dr. Diego Ramirez', 'diego.ramirez@example.com', 'clave_demo_04'),
(5, 'Dra. Camila Torres', 'camila.torres@example.com', 'clave_demo_05'),
(6, 'Felipe Morales', 'felipe.morales@example.com', 'clave_demo_06'),
(7, 'Valentina Rojas', 'valentina.rojas@example.com', 'clave_demo_07'),
(8, 'Jorge Muñoz', 'jorge.munoz@example.com', 'clave_demo_08'),
(9, 'Daniela Silva', 'daniela.silva@example.com', 'clave_demo_09'),
(10, 'Pablo Contreras', 'pablo.contreras@example.com', 'clave_demo_10'),
(11, 'Camila Fernanda Rojas Soto', 'camila.rojas@turnomed.cl', 'clave_demo_11'),
(12, 'Matías Ignacio Valdés Muñoz', 'matias.valdes@turnomed.cl', 'clave_demo_12'),
(13, 'Valentina Paz Contreras Silva', 'valentina.contreras@turnomed.cl', 'clave_demo_13'),
(14, 'Sebastián Andrés Morales Pinto', 'sebastian.morales@turnomed.cl', 'clave_demo_14'),
(15, 'Francisca Javiera Herrera Díaz', 'francisca.herrera@turnomed.cl', 'clave_demo_15');

-- 4. enfermero
INSERT INTO enfermero (id_usuario, nombre, rut, telefono, area) VALUES
(11, 'Camila Fernanda Rojas Soto', '19458321-1','+56984123901', 'Urgencias'),
(12, 'Matías Ignacio Valdés Muñoz', '18734912-0', '+56975234812', 'UCI Adulto'),
(13, 'Valentina Paz Contreras Silva', '20194856-5', '+56991345723', 'Pediatría'),
(14, 'Sebastián Andrés Morales Pinto', '17629483-5', NULL, 'Pabellón Quirúrgico'),
(15, 'Francisca Javiera Herrera Díaz', '21045789-4', '+56962456934', 'Medicina Interna');

-- 5. pacientes
INSERT INTO pacientes (id_usuario, nombre_paciente, rut, telefono, id_direccion) VALUES
(6, 'Felipe Morales', '16.666.666-6', '+56966666666', 6),
(7, 'Valentina Rojas', '17.777.777-7', '+56977777777', 7),
(8, 'Jorge Muñoz', '18.888.888-8', '+56988888888', 8),
(9, 'Daniela Silva', '19.999.999-9', '+56999999999', 9),
(10, 'Pablo Contreras', '10.101.010-1', '+56910101010', 10);

-- 6. Medico
INSERT INTO Medico (id_usuario, nombre_medico, numero_formacion, id_especialidad) VALUES
(1,'Dra. Ana Perez', 'REG-MED-001', 1),
(2, 'Dr. Carlos Soto', 'REG-MED-002', 2),
(3, 'Dra. Maria Gonzalez', 'REG-MED-003', 3),
(4, 'Dr. Diego Ramirez', 'REG-MED-004', 4),
(5, 'Dra. Camila Torres', 'REG-MED-005', 5);

-- 7. Agenda
INSERT INTO Agenda (id_agenda, jornada_laboral) VALUES
(1, 'Lunes a viernes, jornada de mañana'),
(2, 'Lunes a viernes, jornada de tarde'),
(3, 'Lunes y miercoles, jornada completa'),
(4, 'Martes y jueves, jornada de mañana'),
(5, 'Lunes a jueves, jornada de tarde'),
(6, 'Lunes a viernes, jornada completa'),
(7, 'Miercoles a viernes, jornada de mañana'),
(8, 'Martes a sabado, jornada de tarde'),
(9, 'Lunes, miercoles y viernes'),
(10, 'Martes y jueves, jornada completa');

-- 8. Horario
INSERT INTO Horario
(id_horario, dia, horario_inicio, horario_fin, disponible, id_agenda, id_medico)
VALUES
(1, 'Lunes', '08:00:00', '12:00:00', TRUE, 1, 1),
(2, 'Martes', '14:00:00', '18:00:00', TRUE, 2, 2),
(3, 'Miercoles', '09:00:00', '13:00:00', TRUE, 3, 3),
(4, 'Jueves', '08:30:00', '12:30:00', TRUE, 4, 4),
(5, 'Viernes', '14:00:00', '18:00:00', TRUE, 5, 5),
(6, 'Lunes', '10:00:00', '16:00:00', FALSE, 6, 1),
(7, 'Martes', '09:00:00', '13:00:00', TRUE, 7, 2),
(8, 'Miercoles', '15:00:00', '19:00:00', TRUE, 8, 3),
(9, 'Jueves', '08:00:00', '12:00:00', TRUE, 9, 4),
(10, 'Viernes', '13:00:00', '17:00:00', TRUE, 10, 5);

-- 9. Turno
INSERT INTO Turno 
(fecha, hora, estado, id_paciente, id_medico, id_agenda) VALUES
('2026-11-02', '08:30:00', 'Reservado', 1, 1, 1),
('2026-11-03', '14:30:00', 'Confirmado', 2, 2, 2),
('2026-11-04', '09:30:00', 'Reservado', 3, 3, 3),
('2026-11-05', '09:00:00', 'Atendido', 4, 4, 4),
('2026-11-06', '15:00:00', 'Confirmado', 5, 5, 5),
('2026-11-09', '10:30:00', 'Cancelado', 1, 1, 6),
('2026-11-10', '09:30:00', 'Reservado', 2, 2, 7),
('2026-11-11', '15:30:00', 'Confirmado', 3, 3, 8),
('2026-11-12', '08:30:00', 'Reservado', 4, 4, 9),
('2026-11-13', '13:30:00', 'Reservado', 5, 5, 10);