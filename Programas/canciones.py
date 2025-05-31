import pandas as pd
import os
from pathlib import Path

#Rutas de archivos
carpeta_actual = Path(__file__).parent #Carpeta Programas
carpeta_proyecto = carpeta_actual.parent #Carpeta Musica Analisis
ruta_salida = carpeta_proyecto / 'Salida'
ruta_artista = carpeta_proyecto / 'Catalogos'
ruta_metadata = ruta_salida / 'metadata.csv'
ruta_artista = ruta_artista / 'artistas.csv'
ruta_canciones = ruta_salida / 'canciones.csv'

# Cargar CSVs
df_meta = pd.read_csv(ruta_metadata, low_memory=False)
df_artista = pd.read_csv(ruta_artista, low_memory=False)

# Join por artista
join_cols = ['Artista']
df_join1 = pd.merge(df_meta, df_artista, on=join_cols, how='left', suffixes=('', '_artista'))

# Detectar filas sin match (por todas las columnas nuevas de itunes = NaN)
columnas_artistas = [c for c in df_artista.columns if c not in join_cols]
sin_match = df_join1[columnas_artistas].isnull().all(axis=1)

# Combinar resultados finales:
df_con_match = df_join1[~sin_match]
df_final = df_con_match

# Recalcular filas sin match finales (opcional)
sin_match_final = df_final[columnas_artistas].isnull().all(axis=1)

# Reemplazar columna 'Artista' con la homologada (si existe)
df_final['Artista'] = df_final['Artista Homologado'].fillna(df_final['Artista'])

# Eliminar columna 'Artista Homologado' para mantener estructura original
df_final = df_final.drop(columns=['Artista Homologado'])

print(f"[CHECK] Total filas: {len(df_final)}")
print(f"[CHECK] Filas sin match finales: {sin_match_final.sum()}")

# Guardar archivo final
df_final.to_csv(ruta_canciones, index=False)
print(f"[OK] Join final guardado en '{ruta_canciones}'")