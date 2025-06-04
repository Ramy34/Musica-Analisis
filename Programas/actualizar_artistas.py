from pathlib import Path
import pandas as pd
import re

carpeta_actual = Path(__file__).parent #Carpeta Programas
carpeta_proyecto = carpeta_actual.parent #Carpeta Musica Analisis
ruta_metadata = carpeta_proyecto / 'Salida'
ruta_artista = carpeta_proyecto / 'Catalogos'
ruta_metadata = ruta_metadata / 'metadata.csv'
ruta_artista = ruta_artista / 'artistas.csv'

# Cargar los archivos CSV
metadata = pd.read_csv(ruta_metadata, low_memory=False)
artista = pd.read_csv(ruta_artista, low_memory=False)

# Asegúrate de que el nombre de la columna sea igual o ajusta left_on / right_on
# Por ejemplo, si es 'Artista' en metadata y 'artist' en artista.csv:
df = metadata[~metadata["Artista"].isin(artista["Artista"])]

# Eliminar duplicados por la columna 'artist'
df = df.drop_duplicates(subset='Artista')

# Separadores: feat o feat., &, x, con, with
separators = ['feat\\.?', '&', 'con', 'with', '/','、']
split_regex = '|'.join(separators)

# Excepciones: artistas que no deben ser separados
comma_exceptions = [
    "Emerson, Lake & Palmer",
    "serpentwithfeet",
    "MAN WITH A MISSION",
    "Kellin from Sleeping With Sirens",
    "KENN with The NaB's",
    "Satoshi (CV- Rica Matsumoto) with my friends",
    "3年E組うた担(渚&茅野&業&磯貝&前原)",
    "3年E組ヌル担(渚&業&寺坂&中村)",
    "Jesse & Joy",
    "Fear, and Loathing in Las Vegas",
    "ConfidentialMX",
    "GuruConnect",
    "5 Seconds of Summer",
    "Luis R Conriquez"
]

# Crear marcador seguro que no se romperá con regex
def make_marker(index):
    return f"__EXC_MARKER_{index}__"

# Lista para filas del nuevo DataFrame
rows = []

for original_artist in df['Artista']:
    clean_artist = str(original_artist)
    temp_artist = clean_artist
    exception_map = {}

    # Reemplazar excepciones por marcadores únicos
    for i, exc in enumerate(comma_exceptions):
        marker = make_marker(i)
        pattern = re.escape(exc)
        if re.search(pattern, temp_artist, flags=re.IGNORECASE):
            temp_artist = re.sub(pattern, marker, temp_artist, flags=re.IGNORECASE)
            exception_map[marker] = exc  # Guardamos cómo restaurar

    # Separar usando los separadores definidos
    parts = re.split(split_regex, temp_artist, flags=re.IGNORECASE)

    final_parts = []
    for part in parts:
        part = part.strip()
        # Si es un marcador, restauramos
        if part in exception_map:
            final_parts.append(exception_map[part])
        else:
            # Separar por coma (solo si no es excepción)
            sub_parts = [p.strip() for p in part.split(',') if p.strip()]
            final_parts.extend(sub_parts)

    for artist in final_parts:
        rows.append({
            'Artista': original_artist,
            'Artista Homologado': artist
        })

# Crear DataFrame final y eliminar duplicados
df_homogenized = pd.DataFrame(rows).drop_duplicates()
nuevos_registros = len(df_homogenized)

# Agregar al archivo sin sobrescribir
df_homogenized.to_csv(ruta_artista, mode='a', index=False, header=False, encoding='utf-8')

print(f"[OK] Se agregaron {nuevos_registros} nuevos artistas a {ruta_artista}")