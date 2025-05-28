import pandas as pd
from pathlib import Path

# Rutas
carpeta_actual = Path(__file__).parent
carpeta_proyecto = carpeta_actual.parent
carpeta_proyecto_salida = carpeta_proyecto / 'Salida'
carpeta_proyecto = carpeta_proyecto / 'Archivos'

archivoMetadata = carpeta_proyecto / 'metadata_sin_limpiar.csv'
output_file = carpeta_proyecto_salida / 'metadata.csv'


# Definir rutas
ruta_csv_final = Path(archivoMetadata)  # Cambia aquí a la ruta de tu archivo final
ruta_salida = Path(output_file)  # Cambia aquí donde quieres guardar el CSV filtrado

# Columnas que quieres conservar
columnas_deseadas = [
    'title', 'artist', 'album', 'album_artist', 'genre', 'date',
    'duration_seconds', 'bpm', 'beaTunes_tempo_COLOR', 'beaTunes_SPECTRUM',
    'beaTunes_COLOR', 'beaTunes_tempo_timbre_COLOR', 'Track ID', 'Kind',
    'Total Time', 'Year', 'Bit Rate', 'Sample Rate', 'Rating', 'Album Rating',
    'Album Rating Computed', 'Normalization', 'File Folder Count',
    'Library Folder Count', 'Play Count', 'Play Date', 'Play Date UTC',
    'Composer', 'Compilation', 'Explicit', 'Rating Computed'
]

# Cargar CSV
df = pd.read_csv(ruta_csv_final)

# Filtrar solo columnas deseadas (si alguna no existe, se ignora)
columnas_existentes = [col for col in columnas_deseadas if col in df.columns]
df_filtrado = df[columnas_existentes]

# Renombrar columna 'Year' a 'year'
df_filtrado = df_filtrado.rename(columns={'year5': 'year'})

# Guardar CSV filtrado
df_filtrado.to_csv(ruta_salida, index=False)
print(f"[OK] Archivo filtrado guardado en {ruta_salida}")
