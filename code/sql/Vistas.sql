-- Creación de las vistas
CREATE OR REPLACE SECURE VIEW VISTA.biblioteca AS
	SELECT
		a.NAME as "Canción",
		a.ARTIST as "Artista",
		a.ALBUM as "Álbum",
		a.ALBUM_ARTIST as "Artista del álbum",
		IFF(a.PLAY_COUNT IS NULL, 0, a.PLAY_COUNT) as "Reproducciones",
		a.GENRE as "Género",
		a.TOTAL_TIME as "Duración minutos",
		a.FILENAME as "Nombre archivo",
		a.ALBUM_RATING as "Calificacion del álbum",
		a.ALBUM_RATING_COMPUTED as "Calificación del álbum computarizado",
		a.ARTWORK_COUNT as "Carátula",
		a.BPM as "Bpm",
		a.BIT_RATE as "Ratio de bit",
		a.COMMENTS as "Comentarios",
		a.COMPILATION as "Compilación",
		a.COMPOSER as "Compositor",
		a.DATE_ADDED as "Fecha de adición",
		a.DATE_MODIFIED as "Fecha de modificación",
		a.DISC_COUNT as "Número de disco",
		a.DISC_NUMBER as "Número de discos",
		a.DISLIKED as "No me gusta",
		a.EXPLICIT as "Explícito",
		a.KIND as "Tipo de archivo",
		IFF(a.LOVED IS NULL, 'No', 'Sí') as "Me Encanta",
		a.MATCHED as "Matched",
		a.NORMALIZATION AS "Normalización",
		a.PERSISTENT_ID AS "Id",
		a.PLAY_DATE as "Fecha de última reproducción",
		a.PLAY_DATE_UTC as "Fecha de última reproducción UTC",
		a.PURCHASED as "Comprado",
		a.RELEASE_DATE as "Fecha de lanzamiento",
		a.SAMPLE_RATE as "Ratio de muestro",
		a.SIZE as "Tamño",
		a.SKIP_COUNT as "Cuenta de saltos",
		a.SKIP_DATE as "Fecha del último salto",	
		a.TRACK_COUNT as "Número canciones álbum",
		a.TRACK_ID as "Id canción",
		a.TRACK_NUMBER as "Número canción álbum",
		a.TRACK_TYPE as "Tipo canción",
		a.YEAR as "Año",
		b.FILEPATH as "Ruta archivo",
		b.DURATION_SECONDS as "Duración segundos",
		b.BEATUNES_TEMPO_COLOR as "Tempo color",
		b.BEATUNES_SPECTRUM as "Espctro",
		b.BEATUNES_COLOR as "Color", 
		b.BEATUNES_TEMPO_TIMBRE_COLOR as "Tempo Timbre Color",
		b.MOOD_DANCEABILITY as "Danzabilidad",
		b.TUNING as "Tuning",
		b.HAS_LYRICS as "Tiene letra",
		b.LYRICS_TEXT as "Letra",
		b.DURATION_SECONDS / 3600 as "Duración horas",
		IFF(a.RATING = 20, '1',
			IFF(a.RATING = 40, '2', 
				IFF(a.RATING = 60, '3', 
					IFF(a.RATING = 80, '4', 
						IFF(a.RATING = 100, '5', '0'
		))))) as "Calificación",
		IFF(b.DURATION_SECONDS <=30.00, '0',
			IFF(b.DURATION_SECONDS > 30.00 AND b.DURATION_SECONDS <= 90.00, '1',
				IFF(b.DURATION_SECONDS > 90.00 AND b.DURATION_SECONDS <= 150.00, '2',
					IFF(b.DURATION_SECONDS > 150.00 AND b.DURATION_SECONDS <= 210.00, '3',
						IFF(b.DURATION_SECONDS > 210.00 AND b.DURATION_SECONDS <= 270.00, '4',
							IFF(b.DURATION_SECONDS > 270.00 AND b.DURATION_SECONDS <= 330.00, '5', 
								IFF(b.DURATION_SECONDS > 330.00 AND b.DURATION_SECONDS <= 390.00, '6', 
									IFF(b.DURATION_SECONDS > 390.00 AND b.DURATION_SECONDS <= 450.00, '7', 
										IFF(b.DURATION_SECONDS > 450.00 AND b.DURATION_SECONDS <= 510.00, '8', '9 o más'
		))))))))) as "Escala de minutos",
		IFF("Calificación" < '5', 'No', 'Sí') as "Me gusta",
		IFF("Reproducciones" > 0, 'Sí', 'No') as "Reproducido",
		IFF("Comentarios" LIKE '%Se encuentra en spotify%', 'Sí', 'No') as "En Spotify"
	FROM 
		RAW.biblioteca a 
	INNER JOIN 
		RAW.metadata b 
	ON 
		a.artist = b.artist 
	AND 
		a.album = b.album  
	AND 
		upper(a.filename) = upper(b.filename);

-- Creamos la vista del resumen del top 25
CREATE OR REPLACE SECURE VIEW VISTA.resumen_favoritas AS
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
	FROM 
		VISTA.BIBLIOTECA a 
	ORDER BY
		"Reproducciones" DESC
	LIMIT 25;

-- Creamos la vista de artistas desnormalizados
CREATE OR REPLACE VIEW VISTA.ARTISTAS AS
	WITH base AS (
		SELECT
			m.artist AS artista_original,
			CASE
				-- Si es excepción, no se divide
				WHEN e.artista IS NOT NULL THEN ARRAY_CONSTRUCT(m.artist)
				-- Si no es excepción, se divide
				ELSE SPLIT(
					REGEXP_REPLACE(
						m.artist,
						'feat\\.?|&|\\bcon\\b|\\bwith\\b|/|、',
						','
					),
					','
				)
			END AS artistas_array

		FROM RAW.METADATA m
		LEFT JOIN ADM.CAT_ARTISTA_EXCEPCIONES e
			ON UPPER(m.artist) = UPPER(e.artista)
	)
	SELECT DISTINCT
		artista_original AS "Artista original",
		TRIM(f.value::string) AS "Artista"
	FROM 
		base,
	LATERAL FLATTEN(input => artistas_array) f
	WHERE 
			TRIM(f.value::string) IS NOT NULL
		AND 
			TRIM(f.value::string) <> '';

-- Creación de la vista de canciones desnormalizazdas
CREATE OR REPLACE SECURE VIEW VISTA.canciones AS
	SELECT
		"Canción",
		b."Artista" AS "Artista",
		"Álbum",
		"Artista original",
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
	FROM 
		VISTA.BIBLIOTECA a
	INNER JOIN 
		VISTA.ARTISTAS b
	ON 
		a."Artista" = b."Artista original";

-- Creación de la vista de playlist
CREATE OR REPLACE SECURE VIEW VISTA.PLAYLIST AS
	SELECT
		a.PLAYLIST AS "Playlist",
		a.NAME AS "Canción",
		a.ARTIST AS "Artista",
		a.ALBUM AS "Álbum",
		a.ALBUM_ARTIST AS "Artista álbum",
		IFF(a.PLAY_COUNT IS NULL, 0, a.PLAY_COUNT) as "Reproducciones",
		a.GENRE AS "Género",
		a.TOTAL_TIME AS "Duración minutos",
		a.FILENAME AS "Nombre archivo",
		a.ALBUM_RATING AS "Calificación álbum",
		a.ALBUM_RATING_COMPUTED AS "Calificación álbum computada",
		a.ARTWORK_COUNT AS "Cantidad carátulas",
		a.BPM AS "BPM",
		a.BIT_RATE AS "Ratio bits",
		a.COMMENTS AS "Comentario",
		a.COMPILATION AS "Compilación",
		a.COMPOSER AS "Compositor",
		a.DATE_ADDED AS "Fecha agregado",
		a.DATE_MODIFIED AS "Fecha modificado",
		a.DISC_NUMBER AS "Número disco",
		a.DISC_COUNT AS "Cantidad discos",
		a.DISLIKED AS "No me gusta",
		a.EXPLICIT AS "Explícito",
		a.KIND AS "Tipo de archivo",
		a.LOCATION AS "Ubicación",
		IFF(a.LOVED IS NULL, 'No', 'Sí') as "Me Encanta",
		a.MATCHED as "Matched",
		a.NORMALIZATION as "Normalización",
		a.PERSISTENT_ID as "Id",
		a.PLAY_DATE as "Fecha de última reproducción",
		a.PLAY_DATE_UTC as "Fecha de última reproducción UTC",
		a.PURCHASED as "Comprado",
		IFF(a.RATING = 20, '1',
			IFF(a.RATING = 40, '2', 
				IFF(a.RATING = 60, '3', 
					IFF(a.RATING = 80, '4', 
						IFF(a.RATING = 100, '5', '0'
		))))) as "Calificación",
		a.RELEASE_DATE as "Fecha de lanzamiento",
		a.SAMPLE_RATE as "Ratio de muestro",
		a.SIZE as "Tamño",
		a.SKIP_COUNT as "Cuenta de saltos",
		a.SKIP_DATE as "Fecha del último salto",
		a.TRACK_COUNT as "Número canciones álbum",
		a.TRACK_ID as "Id canción",
		a.TRACK_NUMBER as "Número canción álbum",
		a.TRACK_TYPE as "Tipo canción",
		a.YEAR as "Año",
		b.FILEPATH as "Ruta archivo",
		b.DURATION_SECONDS as "Duración segundos",
		b.BEATUNES_TEMPO_COLOR as "Tempo color",
		b.BEATUNES_SPECTRUM as "Espctro",
		b.BEATUNES_COLOR as "Color", 
		b.BEATUNES_TEMPO_TIMBRE_COLOR as "Tempo Timbre Color",
		b.MOOD_DANCEABILITY as "Danzabilidad",
		b.TUNING as "Tuning",
		b.HAS_LYRICS as "Tiene letra",
		b.LYRICS_TEXT as "Letra",
		b.DURATION_SECONDS / 3600 as "Duración horas",
		IFF(b.DURATION_SECONDS <=30.00, '0',
			IFF(b.DURATION_SECONDS > 30.00 AND b.DURATION_SECONDS <= 90.00, '1',
				IFF(b.DURATION_SECONDS > 90.00 AND b.DURATION_SECONDS <= 150.00, '2',
					IFF(b.DURATION_SECONDS > 150.00 AND b.DURATION_SECONDS <= 210.00, '3',
						IFF(b.DURATION_SECONDS > 210.00 AND b.DURATION_SECONDS <= 270.00, '4',
							IFF(b.DURATION_SECONDS > 270.00 AND b.DURATION_SECONDS <= 330.00, '5', 
								IFF(b.DURATION_SECONDS > 330.00 AND b.DURATION_SECONDS <= 390.00, '6', 
									IFF(b.DURATION_SECONDS > 390.00 AND b.DURATION_SECONDS <= 450.00, '7', 
										IFF(b.DURATION_SECONDS > 450.00 AND b.DURATION_SECONDS <= 510.00, '8', '9 o más'
		))))))))) as "Escala de minutos",
		IFF("Calificación" < '5', 'No', 'Sí') as "Me gusta",
		IFF("Reproducciones" > 0, 'Sí', 'No') as "Reproducido"
	FROM 
		MUSICA.RAW.PLAYLIST a
	INNER JOIN
		MUSICA.RAW.METADATA b
	ON 
		a.ARTIST = b.ARTIST 
	AND 
		a.ALBUM = b.ALBUM  
	AND 
		upper(a.FILENAME) = upper(b.FILENAME);
-- Creación de la vista de artistas sin playlist
CREATE OR REPLACE SECURE VIEW VISTA.ARTISTAS_SIN_PLAYLIST AS
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
	FROM 
		VISTA.CANCIONES 
	WHERE 
		upper("Artista") NOT IN (
			SELECT 
				upper("Playlist") 
			FROM 
				VISTA.PLAYLIST 
			WHERE 
				"Playlist" NOT LIKE '%Concierto%' 
			GROUP BY 
				upper("Playlist") 
			ORDER BY upper("Playlist")
		);
-- Creación de la vista de resumen por artista
CREATE OR REPLACE VIEW VISTA.ARTISTA_RESUMEN AS
	SELECT 
		"Artista", 
		count("Canción") AS "Total de canciones",
		SUM("Reproducciones") AS "Total de reproducciones",
		AVG("Bpm") AS "Bpm promedio",
		AVG("Ratio de bit") AS "Bit rate promedio",
		AVG("Ratio de muestro") AS "Ratio de muestreo promedio",
		SUM(iff("Me gusta" = 'Sí', 1, 0)) AS "Cantidad de favoritas",
		MAX(iff("Playlist" IS NOT NULL, 'Sí', 'No')) AS "Tiene playlist"
	FROM 
		VISTA.CANCIONES
	LEFT JOIN
		(SELECT "Playlist" FROM VISTA.PLAYLIST WHERE "Playlist" NOT LIKE 'Concierto%' GROUP BY "Playlist")
	ON
		UPPER("Artista") = UPPER("Playlist")
	GROUP BY 
		"Artista" 
	ORDER BY 
		"Total de canciones" DESC;