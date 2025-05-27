import pandas as pd
import os
from pathlib import Path

# Ruta del transformacion.py actual
carpeta_actual = Path(__file__).parent
# Subir a la raíz del proyecto
carpeta_proyecto = carpeta_actual.parent
# Ruta del archivo XML y CSV
carpeta_proyecto_salida = carpeta_proyecto / 'Salida'
# Ruta del archivo XML y CSV
carpeta_proyecto = carpeta_proyecto / 'Archivos'
# Nombre del archivo XML y CSV
archivoScript = carpeta_proyecto / 'metadata_sin_limpiar.csv'
archivoiTunes = carpeta_proyecto /'itunes_tracks.csv'
output_file = carpeta_proyecto_salida / 'metadata.csv'
# Cargar los CSVs
df_meta = pd.read_csv(archivoScript)
df_itunes = pd.read_csv(archivoiTunes)

# Normalizar y hacer join (ejemplo usando filename)
df_itunes['filename'] = df_itunes['Location'].apply(lambda x: x.split('/')[-1])
df_final = pd.merge(df_meta, df_itunes, on='filename', how='left')

# Guardar el CSV final
df_final.to_csv(output_file, index=False)
print(f"[OK] Join completado y guardado en '{output_file}'")

# Eliminar archivos originales
try:
    os.remove(archivoScript)
    os.remove(archivoiTunes)
    print("[CLEAN] Archivos originales eliminados.")
except Exception as e:
    print(f"[WARNING] Error al borrar archivos: {e}")
