-- Correr este script después de haber cargado los datos en la base de datos para crear las vistas necesarias para el análisis.
-- Creacion de las vistas
CREATE OR REPLACE VIEW vista.biblioteca AS
WITH base AS (
    SELECT
        COALESCE(a.name, 'null') AS "Canción",
        a.artist AS "Artista",
        a.album AS "Álbum",
        a.album_artist AS "Artista del álbum",
        COALESCE(a.play_count::NUMERIC, 0) AS "Reproducciones",
        a.genre AS "Género",
        a.total_time AS "Duración minutos",
        a.filename AS "Nombre archivo",
        a.album_rating AS "Calificacion del álbum",
        a.album_rating_computed AS "Calificación del álbum computarizado",
        a.artwork_count AS "Carátula",
        COALESCE(a.bpm::NUMERIC, 0) AS "Bpm",
        a.bit_rate AS "Ratio de bit",
        a.comments AS "Comentarios",
        a.compilation AS "Compilación",
        a.composer AS "Compositor",
        a.date_added AS "Fecha de adición",
        a.date_modified AS "Fecha de modificación",
        a.disc_count AS "Número de disco",
        a.disc_number AS "Número de discos",
        a.disliked AS "No me gusta",
        a.explicit AS "Explícito",
        a.kind AS "Tipo de archivo",
        CASE WHEN a.loved IS NULL THEN 'No' ELSE 'Sí' END AS "Me Encanta",
        a.matched AS "Matched",
        a.normalization AS "Normalización",
        a.persistent_id AS "Id",
        a.play_date AS "Fecha de última reproducción",
        a.play_date_utc AS "Fecha de última reproducción UTC",
        a.purchased AS "Comprado",
        a.release_date AS "Fecha de lanzamiento",
        a.sample_rate AS "Ratio de muestro",
        a.size AS "Tamño",
        a.skip_count AS "Cuenta de saltos",
        a.skip_date AS "Fecha del último salto",
        a.track_count AS "Número canciones álbum",
        a.track_id AS "Id canción",
        a.track_number AS "Número canción álbum",
        a.track_type AS "Tipo canción",
        a.year AS "Año",
        b.filepath AS "Ruta archivo",
        b.duration_seconds::NUMERIC AS "Duración segundos",
        b.beatunes_tempo_color AS "Tempo color",
        b.beatunes_spectrum AS "Espctro",
        b.beatunes_color AS "Color",
        b.beatunes_tempo_timbre_color AS "Tempo Timbre Color",
        b.mood_danceability::NUMERIC AS "Danzabilidad",
        b.tuning AS "Tuning",
        b.has_lyrics AS "Tiene letra",
        b.lyrics_text AS "Letra",
        b.duration_seconds::NUMERIC / 3600.0 AS "Duración horas",
        CASE a.rating::NUMERIC
            WHEN 20 THEN '1'
            WHEN 40 THEN '2'
            WHEN 60 THEN '3'
            WHEN 80 THEN '4'
            WHEN 100 THEN '5'
            ELSE '0'
        END AS "Calificación",
        CASE
            WHEN b.duration_seconds::NUMERIC <= 30.00 THEN '0'
            WHEN b.duration_seconds::NUMERIC <= 90.00 THEN '1'
            WHEN b.duration_seconds::NUMERIC <= 150.00 THEN '2'
            WHEN b.duration_seconds::NUMERIC <= 210.00 THEN '3'
            WHEN b.duration_seconds::NUMERIC <= 270.00 THEN '4'
            WHEN b.duration_seconds::NUMERIC <= 330.00 THEN '5'
            WHEN b.duration_seconds::NUMERIC <= 390.00 THEN '6'
            WHEN b.duration_seconds::NUMERIC <= 450.00 THEN '7'
            WHEN b.duration_seconds::NUMERIC <= 510.00 THEN '8'
            ELSE '9 o más'
        END AS "Escala de minutos"
    FROM raw.biblioteca a
    INNER JOIN raw.metadata b
        ON a.artist = b.artist
       AND a.album = b.album
       AND UPPER(a.filename) = UPPER(b.filename)
)
SELECT
    base.*,
    CASE WHEN base."Calificación" < '5' THEN 'No' ELSE 'Sí' END AS "Me gusta",
    CASE WHEN base."Reproducciones" > 0 THEN 'Sí' ELSE 'No' END AS "Reproducido",
    CASE WHEN base."Comentarios" LIKE '%Se encuentra en spotify%' THEN 'Sí' ELSE 'No' END AS "En Spotify"
FROM base;

-- Creamos la vista del resumen del top 25
CREATE OR REPLACE VIEW vista.resumen_favoritas AS
SELECT
    "Canción",
    "Artista",
    "Álbum",
    "Artista del álbum",
    "Reproducciones",
    "Género",
    "Duración minutos",
    "Nombre archivo",
    "Calificacion del álbum",
    "Calificación del álbum computarizado",
    "Carátula",
    "Bpm",
    "Ratio de bit",
    "Comentarios",
    "Compilación",
    "Compositor",
    "Fecha de adición",
    "Fecha de modificación",
    "Número de disco",
    "Número de discos",
    "No me gusta",
    "Explícito",
    "Tipo de archivo",
    "Me Encanta",
    "Matched",
    "Normalización",
    "Id",
    "Fecha de última reproducción",
    "Fecha de última reproducción UTC",
    "Comprado",
    "Fecha de lanzamiento",
    "Ratio de muestro",
    "Tamño",
    "Cuenta de saltos",
    "Fecha del último salto",
    "Número canciones álbum",
    "Id canción",
    "Número canción álbum",
    "Tipo canción",
    "Año",
    "Ruta archivo",
    "Duración segundos",
    "Tempo color",
    "Espctro",
    "Color",
    "Tempo Timbre Color",
    "Danzabilidad",
    "Tuning",
    "Tiene letra",
    "Letra",
    "Duración horas",
    "Calificación",
    "Escala de minutos",
    "Me gusta",
    "Reproducido",
    "En Spotify"
FROM vista.biblioteca
ORDER BY "Reproducciones" DESC
LIMIT 25;

-- Creamos la vista de artistas desnormalizados
CREATE OR REPLACE VIEW vista.artistas AS
WITH RECURSIVE protegidos AS (

    -- Registro base
    SELECT
        m.artist AS artista_original,
        m.artist AS artist_protegido,
        1 AS idx
    FROM raw.metadata m

    UNION ALL

    -- Vamos protegiendo cada excepción
    SELECT
        p.artista_original,

        REPLACE(
            p.artist_protegido,
            e.artista,

            -- Reemplazamos separadores peligrosos
            REPLACE(
                REPLACE(
                    REPLACE(
                        REPLACE(
                            REPLACE(
                                e.artista,
                                '&', '__AMP__'
                            ),
                            ',', '__COMMA__'
                        ),
                        '/', '__SLASH__'
                    ),
                    ' with ', '__WITH__'
                ),
                ' con ', '__CON__'
            )
        ) AS artist_protegido,

        idx + 1

    FROM protegidos p
    JOIN (
        SELECT
            ROW_NUMBER() OVER () AS rn,
            artista
        FROM adm.cat_artista_excepciones
    ) e
        ON e.rn = p.idx
),

final_protegido AS (
    SELECT DISTINCT ON (artista_original)
        artista_original,
        artist_protegido
    FROM protegidos
    ORDER BY artista_original, idx DESC
),

base AS (
    SELECT
        artista_original,

        string_to_array(
            regexp_replace(
                artist_protegido,
                'feat\.?|&|\mcon\M|\mwith\M|/|、',
                ',',
                'gi'
            ),
            ','
        ) AS artistas_array

    FROM final_protegido
)

SELECT DISTINCT
    artista_original AS "Artista original",

    TRIM(
        REPLACE(
            REPLACE(
                REPLACE(
                    REPLACE(
                        REPLACE(
                            f.value,
                            '__AMP__', '&'
                        ),
                        '__COMMA__', ','
                    ),
                    '__SLASH__', '/'
                ),
                '__WITH__', ' with '
            ),
            '__CON__', ' con '
        )
    ) AS "Artista"

FROM base
CROSS JOIN LATERAL unnest(artistas_array) AS f(value)

WHERE
    TRIM(f.value) IS NOT NULL
    AND TRIM(f.value) <> '';

-- Creacion de la vista de canciones desnormalizadas
CREATE OR REPLACE VIEW vista.canciones AS
SELECT
    a."Canción",
    b."Artista" AS "Artista",
    a."Álbum",
    b."Artista original",
    a."Artista del álbum",
    a."Reproducciones",
    a."Género",
    a."Duración minutos",
    a."Nombre archivo",
    a."Calificacion del álbum",
    a."Calificación del álbum computarizado",
    a."Carátula",
    a."Bpm",
    a."Ratio de bit",
    a."Comentarios",
    a."Compilación",
    a."Compositor",
    a."Fecha de adición",
    a."Fecha de modificación",
    a."Número de disco",
    a."Número de discos",
    a."No me gusta",
    a."Explícito",
    a."Tipo de archivo",
    a."Me Encanta",
    a."Matched",
    a."Normalización",
    a."Id",
    a."Fecha de última reproducción",
    a."Fecha de última reproducción UTC",
    a."Comprado",
    a."Fecha de lanzamiento",
    a."Ratio de muestro",
    a."Tamño",
    a."Cuenta de saltos",
    a."Fecha del último salto",
    a."Número canciones álbum",
    a."Id canción",
    a."Número canción álbum",
    a."Tipo canción",
    a."Año",
    a."Ruta archivo",
    a."Duración segundos",
    a."Tempo color",
    a."Espctro",
    a."Color",
    a."Tempo Timbre Color",
    a."Danzabilidad",
    a."Tuning",
    a."Tiene letra",
    a."Letra",
    a."Duración horas",
    a."Calificación",
    a."Escala de minutos",
    a."Me gusta",
    a."Reproducido",
    a."En Spotify"
FROM vista.biblioteca a
INNER JOIN vista.artistas b
    ON a."Artista" = b."Artista original";

-- Creacion de la vista de playlist
CREATE OR REPLACE VIEW vista.playlist AS
WITH base AS (
    SELECT
        a.playlist AS "Playlist",
        COALESCE(a.name, 'null') AS "Canción",
        a.artist AS "Artista",
        a.album AS "Álbum",
        a.album_artist AS "Artista álbum",
        COALESCE(a.play_count::NUMERIC, 0) AS "Reproducciones",
        a.genre AS "Género",
        a.total_time AS "Duración minutos",
        a.filename AS "Nombre archivo",
        a.album_rating AS "Calificación álbum",
        a.album_rating_computed AS "Calificación álbum computada",
        a.artwork_count AS "Cantidad carátulas",
        a.bpm AS "BPM",
        a.bit_rate AS "Ratio bits",
        a.comments AS "Comentario",
        a.compilation AS "Compilación",
        a.composer AS "Compositor",
        a.date_added AS "Fecha agregado",
        a.date_modified AS "Fecha modificado",
        a.disc_number AS "Número disco",
        a.disc_count AS "Cantidad discos",
        a.disliked AS "No me gusta",
        a.explicit AS "Explícito",
        a.kind AS "Tipo de archivo",
        a.location AS "Ubicación",
        CASE WHEN a.loved IS NULL THEN 'No' ELSE 'Sí' END AS "Me Encanta",
        a.matched AS "Matched",
        a.normalization AS "Normalización",
        a.persistent_id AS "Id",
        a.play_date AS "Fecha de última reproducción",
        a.play_date_utc AS "Fecha de última reproducción UTC",
        a.purchased AS "Comprado",
        CASE a.rating::NUMERIC
            WHEN 20 THEN '1'
            WHEN 40 THEN '2'
            WHEN 60 THEN '3'
            WHEN 80 THEN '4'
            WHEN 100 THEN '5'
            ELSE '0'
        END AS "Calificación",
        a.release_date AS "Fecha de lanzamiento",
        a.sample_rate AS "Ratio de muestro",
        a.size AS "Tamño",
        a.skip_count AS "Cuenta de saltos",
        a.skip_date AS "Fecha del último salto",
        a.track_count AS "Número canciones álbum",
        a.track_id AS "Id canción",
        a.track_number AS "Número canción álbum",
        a.track_type AS "Tipo canción",
        a.year AS "Año",
        b.filepath AS "Ruta archivo",
        b.duration_seconds AS "Duración segundos",
        b.beatunes_tempo_color AS "Tempo color",
        b.beatunes_spectrum AS "Espctro",
        b.beatunes_color AS "Color",
        b.beatunes_tempo_timbre_color AS "Tempo Timbre Color",
        b.mood_danceability AS "Danzabilidad",
        b.tuning AS "Tuning",
        b.has_lyrics AS "Tiene letra",
        b.lyrics_text AS "Letra",
        b.duration_seconds::NUMERIC / 3600.0 AS "Duración horas",
        CASE
            WHEN b.duration_seconds::NUMERIC <= 30.00 THEN '0'
            WHEN b.duration_seconds::NUMERIC <= 90.00 THEN '1'
            WHEN b.duration_seconds::NUMERIC <= 150.00 THEN '2'
            WHEN b.duration_seconds::NUMERIC <= 210.00 THEN '3'
            WHEN b.duration_seconds::NUMERIC <= 270.00 THEN '4'
            WHEN b.duration_seconds::NUMERIC <= 330.00 THEN '5'
            WHEN b.duration_seconds::NUMERIC <= 390.00 THEN '6'
            WHEN b.duration_seconds::NUMERIC <= 450.00 THEN '7'
            WHEN b.duration_seconds::NUMERIC <= 510.00 THEN '8'
            ELSE '9 o más'
        END AS "Escala de minutos"
    FROM raw.playlist a
    INNER JOIN raw.metadata b
        ON a.artist = b.artist
       AND a.album = b.album
       AND UPPER(a.filename) = UPPER(b.filename)
)
SELECT
    base.*,
    CASE WHEN base."Calificación" < '5' THEN 'No' ELSE 'Sí' END AS "Me gusta",
    CASE WHEN base."Reproducciones" > 0 THEN 'Sí' ELSE 'No' END AS "Reproducido"
FROM base;

-- Creacion de la vista de artistas sin playlist
CREATE OR REPLACE VIEW vista.artistas_sin_playlist AS
SELECT
    "Canción",
    "Artista",
    "Álbum",
    "Artista original",
    "Género",
    "Duración minutos",
    "Nombre archivo",
    "Artista del álbum",
    "Calificacion del álbum",
    "Calificación del álbum computarizado",
    "Carátula",
    "Bpm",
    "Ratio de bit",
    "Comentarios",
    "Compilación",
    "Compositor",
    "Fecha de adición",
    "Fecha de modificación",
    "Número de disco",
    "Número de discos",
    "No me gusta",
    "Explícito",
    "Tipo de archivo",
    "Me Encanta",
    "Matched",
    "Normalización",
    "Id",
    "Fecha de última reproducción",
    "Fecha de última reproducción UTC",
    "Comprado",
    "Fecha de lanzamiento",
    "Ratio de muestro",
    "Tamño",
    "Cuenta de saltos",
    "Fecha del último salto",
    "Número canciones álbum",
    "Id canción",
    "Número canción álbum",
    "Tipo canción",
    "Año",
    "Ruta archivo",
    "Duración segundos",
    "Tempo color",
    "Espctro",
    "Color",
    "Tempo Timbre Color",
    "Danzabilidad",
    "Tuning",
    "Tiene letra",
    "Letra",
    "Reproducciones",
    "Duración horas",
    "Calificación",
    "Escala de minutos",
    "Me gusta",
    "Reproducido",
    "En Spotify"
FROM vista.canciones
WHERE UPPER("Artista") NOT IN (
    SELECT UPPER("Playlist")
    FROM vista.playlist
    WHERE "Playlist" NOT LIKE '%Concierto%'
    GROUP BY UPPER("Playlist")
);

-- Creacion de la vista de resumen por artista
CREATE OR REPLACE VIEW vista.artista_resumen AS
SELECT
    c."Artista",
    COUNT(c."Canción") AS "Total de canciones",
    SUM(c."Reproducciones") AS "Total de reproducciones",
    SUM(CASE WHEN c."Me gusta" = 'Sí' THEN 1 ELSE 0 END) AS "Cantidad de favoritas",
    ROUND(SUM(CASE WHEN c."Me gusta" = 'Sí' THEN 1 ELSE 0 END)::NUMERIC / COUNT(c."Canción")::NUMERIC * 100, 2) AS "% favoritas",
    ROUND(SUM(CASE WHEN c."Reproducido" = 'Sí' THEN 1 ELSE 0 END)::NUMERIC / COUNT(c."Canción")::NUMERIC * 100, 2) AS "% reproducidas",
    ROUND(SUM(CASE WHEN c."Tiene letra" = 'Sí' THEN 1 ELSE 0 END)::NUMERIC / COUNT(c."Canción")::NUMERIC * 100, 2) AS "% con letra",
    COALESCE(ROUND(SUM(CASE WHEN c."Me gusta" = 'Sí' AND c."Tiene letra" = 'Sí' THEN 1 ELSE 0 END)::NUMERIC / NULLIF(SUM(CASE WHEN c."Me gusta" = 'Sí' THEN 1 ELSE 0 END), 0)::NUMERIC * 100, 2), 0) AS "% con letra favoritas",
    TRUNC(AVG(c."Bpm"::NUMERIC), 2) AS "Bpm promedio",
    TRUNC(AVG(c."Ratio de bit"::NUMERIC), 2) AS "Bit rate promedio",
    TRUNC(AVG(c."Ratio de muestro"::NUMERIC), 2) AS "Ratio de muestreo promedio", 
    MAX(CASE WHEN p."Playlist" IS NOT NULL THEN 'Sí' ELSE 'No' END) AS "Tiene playlist",
    COALESCE(p."Total de canciones playlist", 0) AS "Total de canciones playlist"
FROM 
    vista.canciones c
LEFT JOIN (
    SELECT
        "Playlist",
        COUNT("Canción") AS "Total de canciones playlist"
    FROM 
        vista.playlist
    WHERE 
        "Playlist" NOT LIKE 'Concierto%'
    GROUP BY 
        "Playlist"
) p
    ON UPPER(c."Artista") = UPPER(p."Playlist")
GROUP BY 
    c."Artista",
    p."Total de canciones playlist"
ORDER BY 
    "Total de canciones" DESC;