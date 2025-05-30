import pandas as pd
import os
from pathlib import Path
import urllib.parse

# Rutas
carpeta_actual = Path(__file__).parent
carpeta_proyecto = carpeta_actual.parent
carpeta_proyecto = carpeta_proyecto / 'Archivos'
archivoScript = carpeta_proyecto / 'metadata_sucia.csv'
archivoiTunes = carpeta_proyecto / 'itunes_tracks.csv'
output_file = carpeta_proyecto / 'metadata_sin_limpiar.csv'
output_file_sin_match = carpeta_proyecto / 'sin_match.csv'

# Funciones para limpiar texto
def clean_text(x):
    if pd.isna(x):
        return ''
    return str(x).lower().strip()

# Normalizar location en itunes
def obtener_filename_itunes(location):
    if pd.isna(location):
        return ''
    location = location.replace('file://localhost/', '')
    location = urllib.parse.unquote(location)
    return os.path.basename(location).strip().lower()

# Cargar CSVs
df_meta = pd.read_csv(archivoScript)
df_itunes = pd.read_csv(archivoiTunes)

# Normalizar nombre de archivo en metadata
df_meta['join_path'] = df_meta['filepath'].apply(lambda x: os.path.basename(str(x)).strip().lower())

# Normalizar nombre de archivo en itunes
df_itunes['join_path'] = df_itunes['Location'].apply(obtener_filename_itunes)

# Limpiar artista y álbum
df_meta['artist_clean'] = df_meta['artist'].apply(clean_text)
df_meta['album_clean'] = df_meta['album'].apply(clean_text)

df_itunes['artist_clean'] = df_itunes['Artist'].apply(clean_text)
df_itunes['album_clean'] = df_itunes['Album'].apply(clean_text)

# Primer join: join_path + artist_clean + album_clean
join_cols = ['join_path', 'artist_clean', 'album_clean']
df_join1 = pd.merge(df_meta, df_itunes, on=join_cols, how='left', suffixes=('', '_itunes'))

# Detectar filas sin match (por todas las columnas nuevas de itunes = NaN)
columnas_itunes = [c for c in df_itunes.columns if c not in join_cols]
sin_match = df_join1[columnas_itunes].isnull().all(axis=1)

# Segundo join para los sin match, solo por join_path
df_meta_sin_match = df_join1[sin_match][df_meta.columns]  # columnas originales de metadata
df_itunes_reduced = df_itunes.drop(columns=['artist_clean', 'album_clean'])  # para merge limpio

df_join2 = pd.merge(df_meta_sin_match, df_itunes_reduced, on='join_path', how='left', suffixes=('', '_itunes'))

# Combinar resultados finales:
df_con_match = df_join1[~sin_match]
df_final = pd.concat([df_con_match, df_join2], ignore_index=True)

# Recalcular filas sin match finales
sin_match_final = df_final[columnas_itunes].isnull().all(axis=1)

print(f"[CHECK] Total filas: {len(df_final)}")
print(f"[CHECK] Filas sin match finales: {sin_match_final.sum()}")

# Guardar filas sin match en CSV aparte
df_final[sin_match_final].to_csv(output_file_sin_match, index=False)
print("[SAVE] Filas sin match guardadas en 'sin_match.csv'")

# Guardar archivo final
df_final.to_csv(output_file, index=False)
print(f"[OK] Join final guardado en '{output_file}'")
