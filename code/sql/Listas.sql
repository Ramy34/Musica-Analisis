-- Archivo de consultas de diversas listas de reproducción
-- Lista con las canciones que se encuentran en Spotify
SELECT 
    * 
FROM 
    VISTA.biblioteca
WHERE
    "En Spotify" = 'Sí'
-- Lista de canciones que no se han reproducido
SELECT 
    *
FROM
    VISTA.biblioteca
WHERE
    "Reproducido" = 'No'
--Lista de canciones favoritas
SELECT 
    *
FROM
    VISTA.BIBLIOTECA
WHERE
    "Me gusta" = 'Sí'
-- Lista de canciones para caminar
SELECT
    *
FROM 
    VISTA.biblioteca
WHERE
        "Me gusta" = 'Sí'
    AND
        "Bpm" BETWEEN 100 AND 120
    AND
        "Danzabilidad" BETWEEN 50 AND 80;