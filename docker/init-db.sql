-- Crear bases de datos
CREATE DATABASE IF NOT EXISTS logindb;
CREATE DATABASE IF NOT EXISTS accesscontroldb;

-- Conectar a LoginDB
\c logindb;

-- Crear tabla Login
CREATE TABLE IF NOT EXISTS login (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_locked BOOLEAN DEFAULT FALSE,
    failed_attempts INTEGER DEFAULT 0,
    lock_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para optimización
CREATE INDEX idx_login_user_id ON login(user_id);
CREATE INDEX idx_login_is_locked ON login(is_locked);

-- Conectar a AccessControlDB
\c accesscontroldb;

-- Crear tabla Access
CREATE TABLE IF NOT EXISTS access (
    id SERIAL PRIMARY KEY,
    employee_id VARCHAR(50) NOT NULL,
    access_datetime TIMESTAMP NOT NULL,
    exit_datetime TIMESTAMP,
    duration_minutes INTEGER,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla Alert
CREATE TABLE IF NOT EXISTS alert (
    id VARCHAR(50) PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    description TEXT NOT NULL,
    code VARCHAR(50) NOT NULL,
    user_id VARCHAR(50),
    employee_id VARCHAR(50),
    severity VARCHAR(20) DEFAULT 'MEDIUM',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para optimización
CREATE INDEX idx_access_employee_id ON access(employee_id);
CREATE INDEX idx_access_datetime ON access(access_datetime);
CREATE INDEX idx_access_status ON access(status);
CREATE INDEX idx_alert_code ON alert(code);
CREATE INDEX idx_alert_timestamp ON alert(timestamp);

-- Insertar usuario administrador por defecto (password: admin123)
INSERT INTO logindb.login (user_id, password) 
VALUES (1, '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy')
ON CONFLICT (user_id) DO NOTHING;
