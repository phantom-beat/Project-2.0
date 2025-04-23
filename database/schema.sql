
CREATE DATABASE IF NOT EXISTS nutriclinic;
USE nutriclinic;

-- Tabla de pacientes
CREATE TABLE pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    documento_identidad VARCHAR(50) UNIQUE NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    genero ENUM('Masculino', 'Femenino', 'Otro') NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de mediciones antropométricas
CREATE TABLE mediciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT,
    peso DECIMAL(5,2),
    talla DECIMAL(5,2),
    perimetro_braquial DECIMAL(5,2),
    perimetro_cefalico DECIMAL(5,2),
    imc DECIMAL(5,2),
    fecha_medicion DATE,
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE
);

-- Tabla de planes alimenticios
CREATE TABLE planes_alimenticios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT,
    descripcion TEXT,
    fecha_inicio DATE,
    fecha_fin DATE,
    documento_url VARCHAR(255),
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE
);
