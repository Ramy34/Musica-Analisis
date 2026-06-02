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

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------