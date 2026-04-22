-- Archivo de consultas de diversas listas de reproduccion

/* Seccion de la carpeta de estadisticas */

-- Lista con las canciones que se encuentran en Spotify
SELECT
    *
FROM vista.biblioteca
WHERE "En Spotify" = 'Sí';

-- Lista de canciones que no se encuentran en Spotify
SELECT
    *
FROM vista.biblioteca
WHERE "En Spotify" = 'No'
  AND "Comentarios" LIKE '%No está en spotify%';

-- Lista de canciones que no se han reproducido
SELECT
    *
FROM vista.biblioteca
WHERE "Reproducido" = 'No';

-- Lista de canciones favoritas todo
SELECT
    *
FROM vista.biblioteca
WHERE "Me gusta" = 'Sí';

/* Seccion de playlists */

-- Lista de favoritas
SELECT
    *
FROM vista.biblioteca
WHERE "Me gusta" = 'Sí'
  AND "Comentarios" !~* 'es live|es acústico|es remix|from the first take';

-- Lista de canciones recien agregadas
SELECT
    *
FROM vista.biblioteca
WHERE "Fecha de adición" >= CURRENT_TIMESTAMP - INTERVAL '30 days'
ORDER BY "Fecha de adición" DESC
LIMIT 25;

-- Lista de canciones que tienen mucho tiempo de no ser reproducidas
SELECT
    *
FROM vista.biblioteca
WHERE "Me gusta" = 'Sí'
  AND "Fecha de última reproducción UTC" < CURRENT_TIMESTAMP - INTERVAL '6 months'
  AND "En Spotify" = 'Sí'
ORDER BY "Fecha de última reproducción UTC" ASC
LIMIT 30;

-- Lista de canciones que se acaban de reproducir
SELECT
    *
FROM vista.biblioteca
WHERE "Fecha de última reproducción UTC" >= CURRENT_TIMESTAMP - INTERVAL '1 month'
ORDER BY "Fecha de última reproducción UTC" DESC
LIMIT 30;

-- Lista de canciones para caminar
SELECT
    *
FROM vista.biblioteca
WHERE "Me gusta" = 'Sí'
  AND "Bpm" BETWEEN 100 AND 120
  AND "Danzabilidad" BETWEEN 50 AND 80;
