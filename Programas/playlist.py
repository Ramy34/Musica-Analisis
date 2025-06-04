from pathlib import Path
import pandas as pd
import os
import plistlib
import csv

carpeta_actual = Path(__file__).parent #Carpeta Programas
carpeta_proyecto = carpeta_actual.parent #Carpeta Musica Analisis
carpeta_playlist = carpeta_proyecto / 'Archivos' / 'Playlist'
carpeta_salida = carpeta_proyecto / 'Salida'
ruta_metadata = carpeta_salida / 'metadata.csv'
ruta_playlist = carpeta_salida / 'playlist.csv'

# Recolectamos todos los tracks y campos únicos
todas_las_canciones = []
campos_unicos = set()

# Columnas que quieres conservar
columnas_deseadas = [
    'Playlist','Canción', 'Artista','Álbum','Artista del Álbum','Género','Fecha','Duración Segundos',
    'bpm','Color Tempo de beaTunes','Espectro de beaTunes','Color de beaTunes','Color Tempo Timbre de beaTunes',
    'Id Pista','Tipo','Tiempo Total','Año','Tasa de Bits','Frecuencia de Muestreo', 'Valoración',
    'Valoración Álbum','Valoración Álbum Computada','Normalización','Cantidad Carpetas Archivo',
    'Cantidad Carpetas Biblioteca','Reproducciones','Fecha de Reproducción','Fecha de Reproducción UTC',
    'Compositor','Compilación','Explícito','Valoración Computada','Bailabilidad','Afinación'
]

# Funciones para limpiar texto
def clean_text(x):
    if pd.isna(x):
        return ''
    return str(x).lower().strip()

# Recorremos cada archivo XML en la carpeta
for nombre_archivo in os.listdir(carpeta_playlist):
    if nombre_archivo.lower().endswith('.xml'):
        ruta_completa = os.path.join(carpeta_playlist, nombre_archivo)

        try:
            with open(ruta_completa, 'rb') as f:
                plist = plistlib.load(f)

            nombre_playlist = plist.get('Playlists', [{}])[0].get('Name', os.path.splitext(nombre_archivo)[0])
            canciones = plist.get('Tracks', {})

            for track in canciones.values():
                track['Playlist'] = nombre_playlist
                todas_las_canciones.append(track)
                campos_unicos.update(track.keys())

        except Exception as e:
            print(f"[Fail] Error procesando '{nombre_archivo}': {e}")

# Ordenamos los campos y agregamos 'Playlist'
campos_ordenados = sorted(campos_unicos)
if 'Playlist' not in campos_ordenados:
    campos_ordenados.append('Playlist')

# Escribimos al CSV
with open(ruta_playlist, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=campos_ordenados)
    writer.writeheader()

    for track in todas_las_canciones:
        fila = {campo: track.get(campo, '') for campo in campos_ordenados}
        writer.writerow(fila)

# Cargar CSV
df_playlist = pd.read_csv(ruta_playlist, low_memory=False)
df_metadata = pd.read_csv(ruta_metadata, low_memory=False)

# Limpiar artista y álbum
df_metadata['artist_clean'] = df_metadata['Artista del Álbum'].apply(clean_text)
df_metadata['album_clean'] = df_metadata['Álbum'].apply(clean_text)
df_metadata['name_clean'] = df_metadata['Canción'].apply(clean_text)

df_playlist['artist_clean'] = df_playlist['Album Artist'].apply(clean_text)
df_playlist['album_clean'] = df_playlist['Album'].apply(clean_text)
df_playlist['name_clean'] = df_playlist['Name'].apply(clean_text)

# Primer join: join_path + artist_clean + album_clean
join_cols = ['name_clean', 'artist_clean', 'album_clean']
df_join = pd.merge(df_playlist, df_metadata, on=join_cols, how='left', suffixes=('', '_metadata'))

# Detectar filas sin match (por todas las columnas nuevas de itunes = NaN)
columnas_metada = [c for c in df_metadata.columns if c not in join_cols]
sin_match = df_join[columnas_metada].isnull().all(axis=1)

# Combinar resultados finales:
df_con_match = df_join[~sin_match]
df_final = df_con_match

# Filtrar solo columnas deseadas (si alguna no existe, se ignora)
columnas_existentes = [col for col in columnas_deseadas if col in df_final.columns]
df_filtrado = df_final[columnas_existentes]

# Guardar CSV filtrado
df_filtrado.to_csv(ruta_playlist, index=False)
print(f"[OK] Exportadas {len(todas_las_canciones)} canciones de {len(os.listdir(carpeta_playlist))} Playlists a '{ruta_playlist}'")
