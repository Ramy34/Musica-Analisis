-- Archivo de consultas de diversas listas de reproducción

/*  Sección de la carpeta de estaditicas */

-- Lista con las canciones que se encuentran en Spotify
SELECT 
    * 
FROM 
    VISTA.biblioteca
WHERE
    "En Spotify" = 'Sí';

-- Lista de canciones que no se encuentran en Spotify
SELECT 
    * 
FROM 
    VISTA.biblioteca
WHERE
        "En Spotify" = 'No'
    AND
        "Comentarios" LIKE '%No está en spotify%';

-- Lista de canciones que no se han reproducido
SELECT 
    *
FROM
    VISTA.biblioteca
WHERE
    "Reproducido" = 'No';

--Lista de canciones favoritas todo
SELECT 
    *
FROM
    VISTA.BIBLIOTECA
WHERE
    "Me gusta" = 'Sí';

/* Sección de playlists */

-- Lista de Favoritas
SELECT 
    *
FROM 
    VISTA.biblioteca
WHERE
        "Me gusta" = 'Sí'
    AND
        "Comentarios" NOT RLIKE 'es live|Es acústico|Es remix|From The First Take';

-- Lista de canciones recien agregadas
SELECT
    *
FROM 
    VISTA.BIBLIOTECA
WHERE
    "Fecha de adición" >= DATEADD(DAY, -30, CURRENT_TIMESTAMP())
ORDER BY 
    "Fecha de adición" DESC
LIMIT 25;

-- Lista de canciones que tienen mucho tiempo de no ser reporducidas
SELECT
    *
FROM 
    VISTA.BIBLIOTECA
WHERE
        "Me gusta" = 'Sí'
    AND
         "Fecha de última reproducción UTC" < DATEADD(MONTH, -6, CURRENT_TIMESTAMP())
    AND
        "En Spotify" = 'Sí'
ORDER BY 
    "Fecha de última reproducción UTC" ASC
LIMIT 30;

-- Lista de canciones que se acaban de reproducir
SELECT
    *
FROM 
    VISTA.BIBLIOTECA
WHERE
         "Fecha de última reproducción UTC" >= DATEADD(MONTH, -1, CURRENT_TIMESTAMP())
ORDER BY 
    "Fecha de última reproducción UTC" DESC
LIMIT 30;





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