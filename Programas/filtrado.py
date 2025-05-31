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
ruta_csv = Path(archivoMetadata)  # Cambia aquí a la ruta de tu archivo final
ruta_salida = Path(output_file)  # Cambia aquí donde quieres guardar el CSV filtrado

# Columnas que quieres conservar
columnas_deseadas = [
    'title', 'Artist', 'album', 'Album Artist', 'genre', 'date',
    'duration_seconds', 'bpm', 'beaTunes_tempo_COLOR', 'beaTunes_SPECTRUM',
    'beaTunes_COLOR', 'beaTunes_tempo_timbre_COLOR', 'Track ID', 'Kind',
    'Total Time', 'Year', 'Bit Rate', 'Sample Rate', 'Rating', 'Album Rating',
    'Album Rating Computed', 'Normalization', 'File Folder Count',
    'Library Folder Count', 'Play Count', 'Play Date', 'Play Date UTC',
    'Composer', 'Compilation', 'Explicit', 'Rating Computed', 'MOOD_DANCEABILITY', 'Tuning'
]

# Cargar CSV
df = pd.read_csv(ruta_csv, low_memory=False)

# Filtrar solo columnas deseadas (si alguna no existe, se ignora)
columnas_existentes = [col for col in columnas_deseadas if col in df.columns]
df_filtrado = df[columnas_existentes]

df_filtrado = df_filtrado.rename(columns={
    'title': 'Canción',
    'Artist': 'Artista',
    'album': 'Álbum',
    'Album Artist': 'Artista del Álbum',
    'genre': 'Género',
    'date': 'Fecha',
    'duration_seconds': 'Duración Segundos',
    'bpm': 'bpm',
    'beaTunes_tempo_COLOR': 'Color Tempo de beaTunes',
    'beaTunes_SPECTRUM': 'Espectro de beaTunes',
    'beaTunes_COLOR': 'Color de beaTunes',
    'beaTunes_tempo_timbre_COLOR': 'Color Tempo Timbre de beaTunes',
    'Track ID': 'Id Pista',
    'Kind': 'Tipo',
    'Total Time': 'Tiempo Total',
    'Year': 'Año',
    'Bit Rate': 'Tasa de Bits',
    'Sample Rate': 'Frecuencia de Muestreo',
    'Rating': 'Valoración',
    'Album Rating': 'Valoración Álbum',
    'Album Rating Computed': 'Valoración Álbum Computada',
    'Normalization': 'Normalización',
    'File Folder Count': 'Cantidad Carpetas Archivo',
    'Library Folder Count': 'Cantidad Carpetas Biblioteca',
    'Play Count': 'Reproducciones',	
    'Play Date': 'Fecha de Reproducción',
    'Play Date UTC': 'Fecha de Reproducción UTC',
    'Composer': 'Compositor',
    'Compilation': 'Compilación',
    'Explicit': 'Explícito',
    'Rating Computed': 'Valoración Computada',
    'MOOD_DANCEABILITY': 'Bailabilidad',
    'Tuning': 'Afinación'
})
# Guardar CSV filtrado
df_filtrado.to_csv(ruta_salida, index=False)
print(f"[OK] Archivo filtrado guardado en {ruta_salida}")
