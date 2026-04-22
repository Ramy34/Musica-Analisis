-- Consulta para obtener todos los registros de la tabla control_playlist ordenados por id en orden ascendente
SELECT *
FROM adm.control_playlist
ORDER BY id ASC;

-- Consulta para contar el numero de elementos por schema_name en la tabla control_playlist, ordenados de mayor a menor
SELECT
    schema_name,
    COUNT(*) AS elementos
FROM adm.control_playlist
GROUP BY schema_name
ORDER BY COUNT(*) DESC;

-- Consulta para saber el numero de columnas que tiene cada tabla en el esquema pre_raw, ordenadas de mayor a menor
SELECT
    table_name,
    COUNT(*)
FROM information_schema.columns
WHERE table_schema = 'pre_raw'
GROUP BY table_name
ORDER BY COUNT(*) DESC;

-- Consulta para saber cuantas veces se repite cada nombre de columna en el esquema pre_raw, ordenadas de mayor a menor
SELECT
    column_name,
    COUNT(*)
FROM information_schema.columns
WHERE table_schema = 'pre_raw'
GROUP BY column_name
ORDER BY COUNT(*) DESC;
