-- Consulta para obtener todos los registros de la tabla CONTROL_PLAYLIST ordenados por ID en orden ascendente
SELECT * FROM MUSICA.ADM.CONTROL_PLAYLIST ORDER BY ID ASC;
-- Consulta para contar el número de elementos por SCHEMA_NAME en la tabla CONTROL_PLAYLIST, ordenados de mayor a menor
SELECT SCHEMA_NAME, COUNT(*) AS ELEMENTOS FROM MUSICA.ADM.CONTROL_PLAYLIST GROUP BY SCHEMA_NAME ORDER BY COUNT(*) DESC;
-- Consulta para saber el número de columnas que tiene cada tabla en el esquema PRE_RAW, ordenadas de mayor a menor
SELECT TABLE_NAME, COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'PRE_RAW' GROUP BY TABLE_NAME ORDER BY COUNT(*) DESC;
-- Consulta para saber cuántas veces se repite cada nombre de columna en el esquema PRE_RAW, ordenadas de mayor a menor
SELECT COLUMN_NAME, COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'PRE_RAW' GROUP BY COLUMN_NAME ORDER BY COUNT(*) DESC;