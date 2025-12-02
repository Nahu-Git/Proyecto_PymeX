-- db/schema.sql

PRAGMA foreign_keys = ON;

-- Tabla de usuarios del sistema (clientes, empresas, admin, etc.)
CREATE TABLE IF NOT EXISTS usuarios (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_usuario  TEXT    NOT NULL UNIQUE,
    contrasena      TEXT    NOT NULL,   -- aquí va el hash, NO la contraseña en texto plano
    rol             TEXT    NOT NULL    -- 'cliente', 'empresa', 'admin', etc.
);

-- Tabla de empresas ISP
CREATE TABLE IF NOT EXISTS empresas (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre          TEXT    NOT NULL,
    rut             TEXT    NOT NULL,
    email_contacto  TEXT
);

-- Tabla de clientes finales
CREATE TABLE IF NOT EXISTS clientes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre      TEXT    NOT NULL,
    rut         TEXT    NOT NULL,
    email       TEXT,
    telefono    TEXT
);

-- Tabla de planes de internet ofrecidos por las empresas
CREATE TABLE IF NOT EXISTS planes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    empresa_id      INTEGER NOT NULL,
    nombre          TEXT    NOT NULL,
    bajada_mbps     REAL    NOT NULL,
    subida_mbps     REAL    NOT NULL,
    contencion      INTEGER NOT NULL,   -- N de la contención 1:N
    precio_clp      INTEGER NOT NULL,
    descripcion     TEXT,
    FOREIGN KEY (empresa_id) REFERENCES empresas(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Contratos de planes entre clientes y empresas
CREATE TABLE IF NOT EXISTS contratos (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id      INTEGER NOT NULL,
    plan_id         INTEGER NOT NULL,
    fecha_inicio    TEXT    NOT NULL,   -- se guarda en formato ISO: 'YYYY-MM-DD'
    fecha_fin       TEXT,               -- puede ser NULL si sigue activo
    estado          TEXT    NOT NULL,   -- 'activo', 'suspendido', 'terminado', etc.
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (plan_id) REFERENCES planes(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- Tabla de indicadores económicos (UF, DÓLAR, UTM, etc.)
CREATE TABLE IF NOT EXISTS indicadores (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre          TEXT    NOT NULL,   -- 'UF', 'DOLAR', 'UTM', ...
    fecha_valor     TEXT    NOT NULL,   -- 'YYYY-MM-DD'
    valor           REAL    NOT NULL,
    UNIQUE (nombre, fecha_valor)        -- evita duplicados del mismo día
);

-- Registro de consultas de indicadores realizadas por usuarios
CREATE TABLE IF NOT EXISTS consultas_indicadores (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    indicador_id    INTEGER NOT NULL,
    usuario_id      INTEGER NOT NULL,
    fecha_consulta  TEXT    NOT NULL,   -- fecha/hora ISO 'YYYY-MM-DDTHH:MM:SS'
    fuente          TEXT    NOT NULL,   -- URL de la API u origen del dato
    FOREIGN KEY (indicador_id) REFERENCES indicadores(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
