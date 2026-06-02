-- Script de inicializacion de la base de datos "musica" para el proyecto de analisis musical.
-- Creacion de la base de datos
CREATE DATABASE musica;

-- Conectate a la base de datos "musica" antes de ejecutar el resto del script.
\connect musica

-- Creacion de los esquemas
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS adm;
CREATE SCHEMA IF NOT EXISTS vista;
CREATE SCHEMA IF NOT EXISTS playlist;

-- Creacion de la tabla de control de las playlist
CREATE TABLE IF NOT EXISTS adm.control_playlist (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT,
    schema_name TEXT,
    records BIGINT,
    insertar BOOLEAN,
    fecha_creacion_csv TIMESTAMP,
    create_date DATE DEFAULT CURRENT_DATE,
    last_update_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS adm.cat_artista_excepciones (
    artista TEXT PRIMARY KEY,
    activo BOOLEAN DEFAULT TRUE,
    fecha_alta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    comentarios TEXT
);

INSERT INTO adm.cat_artista_excepciones (artista, comentarios)
VALUES
('Emerson, Lake & Palmer', 'Nombre de banda con coma'),
('serpentwithfeet', 'Nombre artistico completo'),
('MAN WITH A MISSION', 'Banda japonesa, nombre fijo'),
('Kellin from Sleeping With Sirens', 'Artista con "from"'),
('KENN with The NaB''s', 'Colaboracion fija'),
('Satoshi (CV- Rica Matsumoto) with my friends', 'Credito oficial'),
('3年E組うた担(渚&茅野&業&磯貝&前原)', 'Grupo anime'),
('3年E組ヌル担(渚&業&寺坂&中村)', 'Grupo anime'),
('Jesse & Joy', 'Duo'),
('Fear, and Loathing in Las Vegas', 'Banda con coma'),
('ConfidentialMX', 'Nombre unico'),
('GuruConnect', 'Nombre unico'),
('5 Seconds of Summer', 'Nombre de banda'),
('Luis R Conriquez', 'Nombre artistico completo'),
('MYTH & ROID', 'Banda japonesa')
ON CONFLICT (artista) DO NOTHING;

CREATE TABLE IF NOT EXISTS adm.cat_comentarios (
    comentario TEXT PRIMARY KEY,
    discrimina_playlist BOOLEAN DEFAULT FALSE
);

INSERT INTO adm.cat_comentarios (comentario, discrimina_playlist)
VALUES
('Se encuentra en spotify', FALSE),
('No está en spotify', FALSE),
('Es acústico', TRUE),
('Es instrumental', TRUE),
('Es remix', TRUE),
('From The First Take', TRUE),
('Es repetida', TRUE),
('Es TV Ver', TRUE),
('Es live', TRUE),
('No es Ado', TRUE)
ON CONFLICT (comentario) DO NOTHING;