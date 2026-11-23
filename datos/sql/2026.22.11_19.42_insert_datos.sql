USE medica_in;

-- 1. Tabla Direccion (10 registros - AUTO_INCREMENT)
INSERT INTO Direccion (calle, comuna, ciudad, numero_casa) VALUES
('Av. Alemania', 'Temuco', 'Temuco', 450),
('Calle Montt', 'Temuco', 'Temuco', 812),
('Av. Providencia', 'Providencia', 'Santiago', 1234),
('Los Carrera', 'Concepción', 'Concepción', 560),
('Av. Valparaíso', 'Viña del Mar', 'Viña del Mar', 310),
('Calle Prat', 'Antofagasta', 'Antofagasta', 920),
('Av. Balmaceda', 'La Serena', 'La Serena', 1505),
('Calle O''Higgins', 'Rancagua', 'Rancagua', 215),
('Av. España', 'Valdivia', 'Valdivia', 740),
('Calle Urmeneta', 'Puerto Montt', 'Puerto Montt', 618);

-- 2. Tabla Especialidad (10 registros - AUTO_INCREMENT)
INSERT INTO Especialidad (nombre_especialidad, descripcion) VALUES
('Medicina General', 'Atención primaria integral y diagnóstico general de pacientes.'),
('Cardiología', 'Diagnóstico y tratamiento de enfermedades del corazón y sistema circulatorio.'),
('Pediatría', 'Atención médica especializada en bebés, niños y adolescentes.'),
('Dermatología', 'Prevención, diagnóstico y tratamiento de enfermedades de la piel.'),
('Neurología', 'Tratamiento de trastornos del sistema nervioso central y periférico.'),
('Traumatología', 'Lesiones y enfermedades del aparato locomotor, huesos y articulaciones.'),
('Ginecología', 'Salud integral del sistema reproductor femenino.'),
('Oftalmología', 'Diagnóstico y tratamiento de patologías oculares y de la visión.'),
('Psiquiatría', 'Evaluación, diagnóstico y tratamiento de trastornos de salud mental.'),
('Endocrinología', 'Trastornos hormonales, metabólicos y de glándulas endocrinas.');

-- 3. Tabla Usuario (10 registros - AUTO_INCREMENT)
-- Nota: Del 1 al 5 serán Pacientes, 6 y 7 Médicos, y del 8 al 10 Enfermeros.
INSERT INTO Usuario (nombre, correo, contrasena, esadministrador) VALUES
('Camila Rojas Soto', 'camila.rojas@email.cl', '680eb27f434bab4f840f9cc39ba3e74e395641f07ebdec6ab495425b562aa88a', 0),
('Matías Silva Muñoz', 'matias.silva@email.cl', '680eb27f434bab4f840f9cc39ba3e74e395641f07ebdec6ab495425b562aa88a', 0),
('Valentina Pérez Díaz', 'valentina.perez@email.cl', '680eb27f434bab4f840f9cc39ba3e74e395641f07ebdec6ab495425b562aa88a', 0),
('Sebastián González Vera', 'sebastian.gonzalez@email.cl', '680eb27f434bab4f840f9cc39ba3e74e395641f07ebdec6ab495425b562aa88a', 0),
('Francisca Morales Pino', 'francisca.morales@email.cl', '680eb27f434bab4f840f9cc39ba3e74e395641f07ebdec6ab495425b562aa88a', 0),
('Dr. Alejandro Vargas Ruiz', 'alejandro.vargas@medicain.cl', '680eb27f434bab4f840f9cc39ba3e74e395641f07ebdec6ab495425b562aa88a', 0),
('Dra. Daniela Castro Lagos', 'daniela.castro@medicain.cl', '680eb27f434bab4f840f9cc39ba3e74e395641f07ebdec6ab495425b562aa88a', 0),
('Sofía Herrera Tapia', 'sofia.herrera@medicain.cl', '680eb27f434bab4f840f9cc39ba3e74e395641f07ebdec6ab495425b562aa88a', 0),
('Diego Fuentes Navarro', 'diego.fuentes@medicain.cl', '680eb27f434bab4f840f9cc39ba3e74e395641f07ebdec6ab495425b562aa88a', 0),
('Constanza Reyes Ortiz', 'constanza.reyes@medicain.cl', '680eb27f434bab4f840f9cc39ba3e74e395641f07ebdec6ab495425b562aa88a', 0);

-- 4. Tabla pacientes (5 registros vinculados a los primeros 5 usuarios)
-- Nota: id_usuario es PK y FK (no es AUTO_INCREMENT en el DDL), por lo que se referencia al ID generado en Usuario.
INSERT INTO pacientes (id_usuario, nombre_paciente, rut, telefono, id_direccion) VALUES
((SELECT id_usuario FROM Usuario WHERE correo = 'camila.rojas@email.cl'), 'Camila Rojas Soto', '18.456.789-1', '+56981234501', 1),
((SELECT id_usuario FROM Usuario WHERE correo = 'matias.silva@email.cl'), 'Matías Silva Muñoz', '17.234.567-8', '+56981234502', 2),
((SELECT id_usuario FROM Usuario WHERE correo = 'valentina.perez@email.cl'), 'Valentina Pérez Díaz', '19.876.543-2', '+56981234503', 3),
((SELECT id_usuario FROM Usuario WHERE correo = 'sebastian.gonzalez@email.cl'), 'Sebastián González Vera', '16.543.210-K', '+56981234504', 4),
((SELECT id_usuario FROM Usuario WHERE correo = 'francisca.morales@email.cl'), 'Francisca Morales Pino', '20.112.233-4', '+56981234505', 5);

-- 5. Tabla Medico (2 registros vinculados a los usuarios 6 y 7)
INSERT INTO Medico (id_usuario, nombre_medico, numero_formacion, id_especialidad) VALUES
((SELECT id_usuario FROM Usuario WHERE correo = 'alejandro.vargas@medicain.cl'), 'Dr. Alejandro Vargas Ruiz', 'REG-MED-45890', 1),
((SELECT id_usuario FROM Usuario WHERE correo = 'daniela.castro@medicain.cl'), 'Dra. Daniela Castro Lagos', 'REG-MED-78123', 2);

-- 6. Tabla enfermero (3 registros vinculados a los usuarios 8, 9 y 10)
INSERT INTO enfermero (id_usuario, nombre, rut, telefono, area) VALUES
((SELECT id_usuario FROM Usuario WHERE correo = 'sofia.herrera@medicain.cl'), 'Sofía Herrera Tapia', '18.990.112-3', '+56977112233', 'Urgencias y Triage'),
((SELECT id_usuario FROM Usuario WHERE correo = 'diego.fuentes@medicain.cl'), 'Diego Fuentes Navarro', '17.665.443-9', '+56977445566', 'Hospitalización General'),
((SELECT id_usuario FROM Usuario WHERE correo = 'constanza.reyes@medicain.cl'), 'Constanza Reyes Ortiz', '19.332.887-5', '+56977889900', 'Pabellón y Cirugía');

-- 7. Tabla Agenda (10 registros - AUTO_INCREMENT)
INSERT INTO Agenda (jornada_laboral) VALUES
('Lunes Mañana (08:00 - 13:00)'),
('Lunes Tarde (14:00 - 19:00)'),
('Martes Mañana (08:00 - 13:00)'),
('Martes Tarde (14:00 - 19:00)'),
('Miércoles Mañana (08:00 - 13:00)'),
('Miércoles Tarde (14:00 - 19:00)'),
('Jueves Mañana (08:00 - 13:00)'),
('Jueves Tarde (14:00 - 19:00)'),
('Viernes Mañana (08:00 - 13:00)'),
('Viernes Tarde (14:00 - 18:00)');

-- 8. Tabla Horario (10 registros - AUTO_INCREMENT)
INSERT INTO Horario (dia, horario_inicio, horario_fin, disponible, id_agenda, id_medico) VALUES
('Lunes', '08:00:00', '13:00:00', TRUE, 1, (SELECT id_usuario FROM Usuario WHERE correo = 'alejandro.vargas@medicain.cl')),
('Lunes', '14:00:00', '19:00:00', TRUE, 2, (SELECT id_usuario FROM Usuario WHERE correo = 'daniela.castro@medicain.cl')),
('Martes', '08:00:00', '13:00:00', TRUE, 3, (SELECT id_usuario FROM Usuario WHERE correo = 'daniela.castro@medicain.cl')),
('Martes', '14:00:00', '19:00:00', TRUE, 4, (SELECT id_usuario FROM Usuario WHERE correo = 'alejandro.vargas@medicain.cl')),
('Miércoles', '08:00:00', '13:00:00', TRUE, 5, (SELECT id_usuario FROM Usuario WHERE correo = 'alejandro.vargas@medicain.cl')),
('Miércoles', '14:00:00', '19:00:00', FALSE, 6, (SELECT id_usuario FROM Usuario WHERE correo = 'daniela.castro@medicain.cl')),
('Jueves', '08:00:00', '13:00:00', TRUE, 7, (SELECT id_usuario FROM Usuario WHERE correo = 'daniela.castro@medicain.cl')),
('Jueves', '14:00:00', '19:00:00', TRUE, 8, (SELECT id_usuario FROM Usuario WHERE correo = 'alejandro.vargas@medicain.cl')),
('Viernes', '08:00:00', '13:00:00', TRUE, 9, (SELECT id_usuario FROM Usuario WHERE correo = 'alejandro.vargas@medicain.cl')),
('Viernes', '14:00:00', '18:00:00', TRUE, 10, (SELECT id_usuario FROM Usuario WHERE correo = 'daniela.castro@medicain.cl'));

-- 9. Tabla Turno (10 registros - AUTO_INCREMENT)
INSERT INTO Turno (fecha, hora, estado, id_paciente, id_medico, id_agenda) VALUES
('2026-11-23', '09:00:00', 'Confirmado', (SELECT id_usuario FROM Usuario WHERE correo = 'camila.rojas@email.cl'), (SELECT id_usuario FROM Usuario WHERE correo = 'alejandro.vargas@medicain.cl'), 1),
('2026-11-23', '15:30:00', 'Reservado', (SELECT id_usuario FROM Usuario WHERE correo = 'matias.silva@email.cl'), (SELECT id_usuario FROM Usuario WHERE correo = 'daniela.castro@medicain.cl'), 2),
('2026-11-24', '10:00:00', 'Atendido', (SELECT id_usuario FROM Usuario WHERE correo = 'valentina.perez@email.cl'), (SELECT id_usuario FROM Usuario WHERE correo = 'daniela.castro@medicain.cl'), 3),
('2026-11-24', '16:00:00', 'Confirmado', (SELECT id_usuario FROM Usuario WHERE correo = 'sebastian.gonzalez@email.cl'), (SELECT id_usuario FROM Usuario WHERE correo = 'alejandro.vargas@medicain.cl'), 4),
('2026-11-25', '11:30:00', 'Cancelado', (SELECT id_usuario FROM Usuario WHERE correo = 'francisca.morales@email.cl'), (SELECT id_usuario FROM Usuario WHERE correo = 'alejandro.vargas@medicain.cl'), 5),
('2026-11-25', '17:00:00', 'Reservado', (SELECT id_usuario FROM Usuario WHERE correo = 'camila.rojas@email.cl'), (SELECT id_usuario FROM Usuario WHERE correo = 'daniela.castro@medicain.cl'), 6),
('2026-11-26', '08:30:00', 'Confirmado', (SELECT id_usuario FROM Usuario WHERE correo = 'matias.silva@email.cl'), (SELECT id_usuario FROM Usuario WHERE correo = 'daniela.castro@medicain.cl'), 7),
('2026-11-26', '15:00:00', 'Reservado', (SELECT id_usuario FROM Usuario WHERE correo = 'valentina.perez@email.cl'), (SELECT id_usuario FROM Usuario WHERE correo = 'alejandro.vargas@medicain.cl'), 8),
('2026-11-27', '12:00:00', 'Confirmado', (SELECT id_usuario FROM Usuario WHERE correo = 'sebastian.gonzalez@email.cl'), (SELECT id_usuario FROM Usuario WHERE correo = 'alejandro.vargas@medicain.cl'), 9),
('2026-11-27', '16:30:00', 'Reservado', (SELECT id_usuario FROM Usuario WHERE correo = 'francisca.morales@email.cl'), (SELECT id_usuario FROM Usuario WHERE correo = 'daniela.castro@medicain.cl'), 10);
