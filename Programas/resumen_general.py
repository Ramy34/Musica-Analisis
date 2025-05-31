from pathlib import Path
import pandas as pd

# Definimos rutas de los archivos
carpeta_actual = Path(__file__).parent #Carpeta Programas
carpeta_proyecto = carpeta_actual.parent #Carpeta Musica Analisis
carpeta_proyecto = carpeta_proyecto / 'Salida'
ruta_metadata = carpeta_proyecto / 'metadata.csv'
ruta_resumen_general = carpeta_proyecto / 'resumen_general.csv'

# Cargamos el archivo CSV con los metadatos
df = pd.read_csv(ruta_metadata, low_memory=False)

#Ordenamos las filas por la columna 'Playcount' de forma descendente
df = df.sort_values(by='Reproducciones', ascending=False)

# seleccionamos las filas que el raiting sea menor de 100
df = df[df['Valoración'] == 100]

#Obtenemos los primeros 25 registros
df = df.head(25)

df.to_csv(ruta_resumen_general, index=False)
print(f"[OK] Resumen general guardado en: {ruta_resumen_general}")