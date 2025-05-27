# Debe de ser el segundo archivo en ejecutarse, ya que es el encargado de convertir el XML de iTunes a CSV
from pathlib import Path
import plistlib
import pandas as pd

# Ruta del transformacion.py actual
carpeta_actual = Path(__file__).parent
# Subir a la raíz del proyecto
carpeta_proyecto = carpeta_actual.parent
# Ruta del archivo XML y CSV
carpeta_proyecto = carpeta_proyecto / 'Archivos'
# Nombre del archivo XML y CSV
archivoXML = carpeta_proyecto / 'Biblioteca.xml'
archivoCSV = carpeta_proyecto / 'itunes_tracks.csv'

# Leer archivo XML
with open(archivoXML, 'rb') as f:
    plist = plistlib.load(f)

tracks = plist['Tracks']
track_list = []

# Convertir los datos a lista de diccionarios
for track_id in tracks:
    track = tracks[track_id]
    track_list.append(track)

# Crear DataFrame y exportar a CSV
df = pd.DataFrame(track_list)
df.to_csv(archivoCSV, index=False)

# Mostrar mensaje con número de canciones
print(f"[OK] Archivo '{archivoCSV.name}' generado con {len(df)} canciones.", flush=True)
