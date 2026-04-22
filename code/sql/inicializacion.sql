-- Creación de la base de datos
CREATE DATABASE MUSICA;
USE MUSICA;
--Creación de los esquemas
CREATE SCHEMA RAW;
CREATE SCHEMA ADM;
CREATE SCHEMA VISTA;
-- Creación de la tabla de control de las playlist
 CREATE OR REPLACE TABLE MUSICA.ADM.CONTROL_PLAYLIST (
	ID NUMBER(38,0) autoincrement start 1 increment 1 noorder,
	NAME VARCHAR(16777216),
	SCHEMA_NAME VARCHAR(16777216),
	RECORDS NUMBER(38,0),
	INSERTAR BOOLEAN,
    FECHA_CREACION_CSV TIMESTAMP,
	CREATE_DATE DATE DEFAULT CURRENT_DATE(),
	LAST_UPDATE_DATE DATE DEFAULT CURRENT_DATE()
);

CREATE OR REPLACE TABLE ADM.CAT_ARTISTA_EXCEPCIONES (
    ARTISTA STRING NOT NULL,
    ACTIVO BOOLEAN DEFAULT TRUE,
    FECHA_ALTA TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    COMENTARIOS STRING
);
INSERT INTO ADM.CAT_ARTISTA_EXCEPCIONES (ARTISTA, COMENTARIOS)
VALUES
('Emerson, Lake & Palmer', 'Nombre de banda con coma'),
('serpentwithfeet', 'Nombre artístico completo'),
('MAN WITH A MISSION', 'Banda japonesa, nombre fijo'),
('Kellin from Sleeping With Sirens', 'Artista con "from"'),
('KENN with The NaB''s', 'Colaboración fija'),
('Satoshi (CV- Rica Matsumoto) with my friends', 'Crédito oficial'),
('3年E組うた担(渚&茅野&業&磯貝&前原)', 'Grupo anime'),
('3年E組ヌル担(渚&業&寺坂&中村)', 'Grupo anime'),
('Jesse & Joy', 'Dúo'),
('Fear, and Loathing in Las Vegas', 'Banda con coma'),
('ConfidentialMX', 'Nombre único'),
('GuruConnect', 'Nombre único'),
('5 Seconds of Summer', 'Nombre de banda'),
('Luis R Conriquez', 'Nombre artístico completo'),
('MYTH & ROID', 'Banda japonesa');
