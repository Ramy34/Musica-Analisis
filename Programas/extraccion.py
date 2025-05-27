# Debe de ser el primer archivo que se ejecute, ya que extrae los metadatos de las canciones y los guarda en un CSV.
# Extrae metadatos de archivos MP3 y M4A y los guarda en un CSV
import os
import csv
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.id3 import TXXX
from mutagen import MutagenError

# Ruta de la carpeta de música
carpeta_musica = r'D:/Compartida/iTunes/iTunes Media/Music'
# Ruta del transformacion.py actual
carpeta_actual = Path(__file__).parent
# Subir a la raíz del proyecto
carpeta_proyecto = carpeta_actual.parent
# Ruta del archivo XML y CSV
carpeta_proyecto = carpeta_proyecto / 'Archivos'
# Nombre del archivo CSV de salida
csv_salida = carpeta_proyecto / 'metadata_sin_limpiar.csv'

campos_csv = [
    'filename', 'filepath', 'title', 'artist', 'album', 'album_artist',
    'genre', 'date', 'year', 'duration_seconds', 'bpm',
    'beaTunes_tempo_COLOR', 'beaTunes_SPECTRUM',
    'beaTunes_COLOR', 'beaTunes_tempo_timbre_COLOR'
]

def extraer_txxx(tags, desc):
    for frame in tags.getall("TXXX"):
        if frame.desc == desc:
            return frame.text[0] if frame.text else ''
    return ''

def limpiar_valor(valor):
    if isinstance(valor, bytes):
        try:
            return valor.decode('utf-8')
        except UnicodeDecodeError:
            return valor.decode('latin1', errors='ignore')
    return valor

def extraer_metadatos_mp3(archivo):
    try:
        audio = MP3(archivo)
        tags = audio.tags or {}

        fecha = str(tags.get('TDRC', [''])[0]) if 'TDRC' in tags else ''
        anio = fecha[:4] if fecha else ''

        return {
            'title': tags.get('TIT2', [''])[0] if 'TIT2' in tags else '',
            'artist': tags.get('TPE1', [''])[0] if 'TPE1' in tags else '',
            'album': tags.get('TALB', [''])[0] if 'TALB' in tags else '',
            'album_artist': tags.get('TPE2', [''])[0] if 'TPE2' in tags else '',
            'genre': tags.get('TCON', [''])[0] if 'TCON' in tags else '',
            'date': fecha,
            'year': anio,
            'duration_seconds': round(audio.info.length, 2),
            'bpm': tags.get('TBPM', [''])[0] if 'TBPM' in tags else '',
            'beaTunes_tempo_COLOR': extraer_txxx(tags, 'beaTunes_tempo_COLOR'),
            'beaTunes_SPECTRUM': extraer_txxx(tags, 'beaTunes_SPECTRUM'),
            'beaTunes_COLOR': extraer_txxx(tags, 'beaTunes_COLOR'),
            'beaTunes_tempo_timbre_COLOR': extraer_txxx(tags, 'beaTunes_tempo_timbre_COLOR'),
        }
    except MutagenError:
        return {}

def extraer_atom_m4a(tags, nombre):
    clave = f'----:com.apple.iTunes:{nombre}'
    valor = tags.get(clave, [''])[0]
    return limpiar_valor(valor)

def extraer_metadatos_m4a(archivo):
    try:
        audio = MP4(archivo)
        tags = audio.tags or {}

        fecha = limpiar_valor(tags.get('©day', [''])[0])
        anio = fecha[:4] if fecha else ''

        return {
            'title': limpiar_valor(tags.get('\xa9nam', [''])[0]),
            'artist': limpiar_valor(tags.get('\xa9ART', [''])[0]),
            'album': limpiar_valor(tags.get('\xa9alb', [''])[0]),
            'album_artist': limpiar_valor(tags.get('aART', [''])[0]),
            'genre': limpiar_valor(tags.get('\xa9gen', [''])[0]),
            'date': fecha,
            'year': anio,
            'duration_seconds': round(audio.info.length, 2),
            'bpm': limpiar_valor(tags.get('tmpo', [''])[0]),
            'beaTunes_tempo_COLOR': extraer_atom_m4a(tags, 'beaTunes_tempo_COLOR'),
            'beaTunes_SPECTRUM': extraer_atom_m4a(tags, 'beaTunes_SPECTRUM'),
            'beaTunes_COLOR': extraer_atom_m4a(tags, 'beaTunes_COLOR'),
            'beaTunes_tempo_timbre_COLOR': extraer_atom_m4a(tags, 'beaTunes_tempo_timbre_COLOR'),
        }
    except MutagenError:
        return {}

# Escanear carpeta
datos_canciones = []

for carpeta_raiz, _, archivos in os.walk(carpeta_musica):
    for archivo in archivos:
        ruta_completa = os.path.join(carpeta_raiz, archivo)
        extension = os.path.splitext(archivo)[1].lower()

        if extension == '.mp3':
            meta = extraer_metadatos_mp3(ruta_completa)
        elif extension == '.m4a':
            meta = extraer_metadatos_m4a(ruta_completa)
        else:
            continue

        if meta:
            meta['filename'] = archivo
            meta['filepath'] = ruta_completa
            datos_canciones.append(meta)

# Guardar CSV
with open(csv_salida, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=campos_csv)
    writer.writeheader()
    writer.writerows(datos_canciones)

print(f"[OK] Metadatos beaTunes exportados a '{csv_salida}' con {len(datos_canciones)} canciones.", flush=True)
