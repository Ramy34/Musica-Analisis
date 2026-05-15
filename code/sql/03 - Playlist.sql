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
    "Artista",
    "Canción",
    "Álbum",
    "Reproducciones",
    "Género",
    "Duración minutos",
    "Artista original",
    "Ruta archivo"
FROM canciones_rankeadas_tmp
WHERE ranking <= 3
ORDER BY
    "Artista",
    ranking;