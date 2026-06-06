CREATE OR REPLACE VIEW playlist.canciones_rankeadas AS
WITH canciones_rankeadas_tmp AS (
    SELECT
        ROW_NUMBER() OVER (
            PARTITION BY c."Artista"
            ORDER BY c."Reproducciones" DESC, c."Canción"
        ) AS ranking,
        c."Artista",
        c."Canción",
        c."Álbum",
        c."Reproducciones",
        c."Género",
        c."Duración minutos",
        c."Artista original",
        c."Ruta archivo"
    FROM vista.canciones c
    INNER JOIN vista.artista_resumen ar
        ON UPPER(c."Artista") = UPPER(ar."Artista")
    WHERE ar."Tiene playlist" = 'Sí'
)

SELECT
    ranking AS "Top",
    "Artista" as "Artista separado",
    "Canción",
    "Álbum",
    "Reproducciones",
    "Género",
    "Duración minutos",
    "Artista original" as "Artista",
    "Ruta archivo"
FROM canciones_rankeadas_tmp
WHERE ranking <= 3
ORDER BY
    "Artista",
    ranking;

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW playlist.nocturna AS
SELECT
    b."Canción",
    b."Artista",
    b."Álbum",
    b."Género",
    b."Bpm",
    b."Danzabilidad",
    b."Color",
    b."Calificación",
    b."Reproducciones",
    b."Duración segundos",
    b."Fecha de última reproducción",
    b."Ruta archivo"
FROM vista.biblioteca b
WHERE 1=1

-- Solo canciones favoritas
AND b."Me gusta" = 'Sí'

AND b."Discrimina playlist" = FALSE

-- Evitar intros/skits
AND b."Duración segundos" >= 150

-- BPM nocturno
AND b."Bpm" BETWEEN 55 AND 120

-- Danzabilidad media-baja
AND b."Danzabilidad" BETWEEN 20 AND 70

-- Géneros compatibles con mood nocturno
AND b."Género" IN (
    'Alternativa',
    'Alternativa & Indie',
    'Alternativa para adultos',
    'Balada',
    'Baladas y boleros',
    'Cantautor',
    'Contemporáneo para adultos',
    'Dance / Electrónica',
    'Dark Cabaret',
    'Electrónica',
    'Folk',
    'Folk alternativo',
    'Instrumental',
    'Jazz',
    'Pop indie',
    'Pop / Rock',
    'R&B / Soul',
    'Soft rock',
    'Soundtrack',
    'Tonada Pop'
)

-- Evitar canciones demasiado agresivas
AND b."Género" NOT IN (
    'Metal',
    'Metalcore',
    'Dubstep',
    'Hard rock',
    'J-Metal',
    'Punk',
    'Rap',
    'Hip-Hop',
    'Hip-Hop / Rap',
    'Rap alternativo',
    'Rap latino'
)

ORDER BY
    CAST(b."Calificación" AS INTEGER) DESC,
    b."Reproducciones" ASC,
    b."Bpm" ASC,
    RANDOM();
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW playlist.entrenamiento AS
SELECT
    b."Canción",
    b."Artista",
    b."Álbum",
    b."Género",
    b."Bpm",
    b."Danzabilidad",
    b."Reproducciones",
    b."Ruta archivo"
FROM vista.biblioteca b
WHERE b."Me gusta" = 'Sí'
  AND b."Discrimina playlist" = FALSE
  AND b."Bpm" >= 120
  AND b."Danzabilidad" >= 60
ORDER BY b."Bpm" DESC, b."Danzabilidad" DESC;
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW playlist.karaoke AS
SELECT
    b."Canción",
    b."Artista",
    b."Álbum",
    b."Género",
    b."Reproducciones",
    b."Ruta archivo"
FROM vista.biblioteca b
WHERE b."Me gusta" = 'Sí'
  AND b."Discrimina playlist" = FALSE
  AND b."Tiene letra" = 'Sí'
  AND b."Reproducciones" >= 15
ORDER BY b."Reproducciones" DESC;
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW playlist.modo_zen AS
SELECT
    b."Canción",
    b."Artista",
    b."Álbum",
    b."Género",
    b."Bpm",
    b."Ruta archivo"
FROM vista.biblioteca b
WHERE b."Discrimina playlist" = FALSE
  AND (b."Comentarios" ILIKE '%Es instrumental%' OR b."Género" IN ('Soundtrack', 'Instrumental', 'Jazz', 'Clásica', 'Lo-Fi', 'Ambient'))
  AND b."Bpm" <= 100
ORDER BY RANDOM()
LIMIT 50;
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW playlist.baul_recuerdos AS
SELECT
    b."Canción",
    b."Artista",
    b."Álbum",
    b."Género",
    b."Fecha de última reproducción",
    b."Reproducciones",
    b."Ruta archivo"
FROM vista.biblioteca b
WHERE b."Me gusta" = 'Sí'
  AND b."Discrimina playlist" = FALSE
  AND b."Fecha de última reproducción UTC"::TIMESTAMP < CURRENT_TIMESTAMP - INTERVAL '1 year'
ORDER BY RANDOM()
LIMIT 50;
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW playlist.segunda_oportunidad AS
SELECT
    b."Canción",
    b."Artista",
    b."Álbum",
    b."Cuenta de saltos",
    b."Fecha del último salto",
    b."Ruta archivo"
FROM vista.biblioteca b
WHERE b."Cuenta de saltos"::NUMERIC > 3
  AND b."Discrimina playlist" = FALSE
ORDER BY b."Cuenta de saltos"::NUMERIC DESC
LIMIT 50;
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW playlist.obsesion_reciente AS
SELECT
    b."Canción",
    b."Artista",
    b."Álbum",
    b."Reproducciones",
    b."Fecha de adición",
    b."Ruta archivo"
FROM vista.biblioteca b
WHERE b."Fecha de adición"::TIMESTAMP >= CURRENT_TIMESTAMP - INTERVAL '3 months'
  AND b."Reproducciones" >= 10
  AND b."Discrimina playlist" = FALSE
ORDER BY b."Reproducciones" DESC;
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW playlist.viajes_epicos AS
SELECT
    b."Canción",
    b."Artista",
    b."Álbum",
    b."Género",
    b."Duración minutos",
    b."Ruta archivo"
FROM vista.biblioteca b
WHERE b."Duración segundos" >= 420
  AND b."Me gusta" = 'Sí'
  AND b."Discrimina playlist" = FALSE
ORDER BY b."Duración segundos" DESC;
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW playlist.vibras_acusticas AS
SELECT
    b."Canción",
    b."Artista",
    b."Álbum",
    b."Género",
    b."Comentarios",
    b."Ruta archivo"
FROM vista.biblioteca b
WHERE b."Comentarios" ILIKE '%Es acústico%'
  AND b."Me gusta" = 'Sí'
ORDER BY RANDOM()
LIMIT 50;
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW playlist.rafaga_corta AS
SELECT
    b."Canción",
    b."Artista",
    b."Álbum",
    b."Duración minutos",
    b."Bpm",
    b."Ruta archivo"
FROM vista.biblioteca b
WHERE b."Duración segundos" <= 150
  AND b."Bpm" >= 130
  AND b."Me gusta" = 'Sí'
  AND b."Discrimina playlist" = FALSE
ORDER BY RANDOM()
LIMIT 50;
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW playlist.exclusivos_locales AS
SELECT
    b."Canción",
    b."Artista",
    b."Álbum",
    b."Género",
    b."Comentarios",
    b."Ruta archivo"
FROM vista.biblioteca b
WHERE b."En Spotify" = 'No'
  AND b."Discrimina playlist" = FALSE
  AND b."Me gusta" = 'Sí'
ORDER BY RANDOM();
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW playlist.viaje_cromatico AS
SELECT
    b."Canción",
    b."Artista",
    b."Álbum",
    b."Color",
    b."Bpm",
    b."Ruta archivo"
FROM vista.biblioteca b
WHERE b."Color" IS NOT NULL AND b."Color" != ''
  AND b."Discrimina playlist" = FALSE
  AND b."Me gusta" = 'Sí'
ORDER BY b."Color" ASC, b."Bpm" ASC;
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW playlist.maquina_tiempo_2000s AS
SELECT
    b."Canción",
    b."Artista",
    b."Álbum",
    b."Año",
    b."Ruta archivo"
FROM vista.biblioteca b
WHERE b."Año" LIKE '200%'
  AND b."Me gusta" = 'Sí'
  AND b."Discrimina playlist" = FALSE
ORDER BY RANDOM()
LIMIT 50;
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------