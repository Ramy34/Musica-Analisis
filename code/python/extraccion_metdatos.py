import os
import csv
import sys
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen import MutagenError
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
import logging

# === Funciones auxiliares ===
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

# === Letras ===
def extraer_letra_mp3(tags):
    """
    Devuelve un dict con:
    - has_lyrics: 'Sí' o 'No'
    - lyrics_text: texto completo (si existe)
    """
    try:
        for frame in tags.getall('USLT'):
            if frame.text and frame.text.strip():
                return {'has_lyrics': 'Sí', 'lyrics_text': frame.text.strip()}
        return {'has_lyrics': 'No', 'lyrics_text': ''}
    except Exception:
        return {'has_lyrics': 'No', 'lyrics_text': ''}

def extraer_letra_m4a(tags):
    """
    Devuelve un dict con:
    - has_lyrics: 'Sí' o 'No'
    - lyrics_text: texto completo (si existe)
    """
    try:
        letra = tags.get('©lyr', [''])
        if letra and isinstance(letra, list):
            letra = letra[0]
        if letra and str(letra).strip():
            return {'has_lyrics': 'Sí', 'lyrics_text': str(letra).strip()}
        return {'has_lyrics': 'No', 'lyrics_text': ''}
    except Exception:
        return {'has_lyrics': 'No', 'lyrics_text': ''}

# === Extracción de metadatos ===
def extraer_metadatos_mp3(archivo):
    try:
        audio = MP3(archivo)
        tags = audio.tags or {}
        fecha = str(tags.get('TDRC', [''])[0]) if 'TDRC' in tags else ''

        letras = extraer_letra_mp3(tags)

        return {
            'title': tags.get('TIT2', [''])[0] if 'TIT2' in tags else '',
            'artist': tags.get('TPE1', [''])[0] if 'TPE1' in tags else '',
            'album': tags.get('TALB', [''])[0] if 'TALB' in tags else '',
            'album_artist': tags.get('TPE2', [''])[0] if 'TPE2' in tags else '',
            'genre': tags.get('TCON', [''])[0] if 'TCON' in tags else '',
            'date': fecha,
            'duration_seconds': round(audio.info.length, 2),
            'bpm': tags.get('TBPM', [''])[0] if 'TBPM' in tags else '',
            'beaTunes_tempo_COLOR': extraer_txxx(tags, 'beaTunes_tempo_COLOR'),
            'beaTunes_SPECTRUM': extraer_txxx(tags, 'beaTunes_SPECTRUM'),
            'beaTunes_COLOR': extraer_txxx(tags, 'beaTunes_COLOR'),
            'beaTunes_tempo_timbre_COLOR': extraer_txxx(tags, 'beaTunes_tempo_timbre_COLOR'),
            'MOOD_DANCEABILITY': extraer_txxx(tags, 'MOOD_DANCEABILITY'),
            'Tuning': extraer_txxx(tags, 'Tuning'),
            'has_lyrics': letras['has_lyrics'],
            'lyrics_text': letras['lyrics_text']
        }
    except Exception as e:
        logging.debug(f"Error extrayendo MP3 {archivo}: {e}")
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

        letras = extraer_letra_m4a(tags)

        return {
            'title': limpiar_valor(tags.get('\xa9nam', [''])[0]),
            'artist': limpiar_valor(tags.get('\xa9ART', [''])[0]),
            'album': limpiar_valor(tags.get('\xa9alb', [''])[0]),
            'album_artist': limpiar_valor(tags.get('aART', [''])[0]),
            'genre': limpiar_valor(tags.get('\xa9gen', [''])[0]),
            'date': fecha,
            'duration_seconds': round(audio.info.length, 2),
            'bpm': limpiar_valor(tags.get('tmpo', [''])[0]),
            'beaTunes_tempo_COLOR': extraer_atom_m4a(tags, 'beaTunes_tempo_COLOR'),
            'beaTunes_SPECTRUM': extraer_atom_m4a(tags, 'beaTunes_SPECTRUM'),
            'beaTunes_COLOR': extraer_atom_m4a(tags, 'beaTunes_COLOR'),
            'beaTunes_tempo_timbre_COLOR': extraer_atom_m4a(tags, 'beaTunes_tempo_timbre_COLOR'),
            'MOOD_DANCEABILITY': extraer_atom_m4a(tags, 'MOOD_DANCEABILITY'),
            'Tuning': extraer_atom_m4a(tags, 'Tuning'),
            'has_lyrics': letras['has_lyrics'],
            'lyrics_text': letras['lyrics_text']
        }
    except Exception as e:
        logging.debug(f"Error extrayendo M4A {archivo}: {e}")
        return {}

# === Procesamiento ===
def procesar_archivo(ruta_completa):
    extension = os.path.splitext(ruta_completa)[1].lower()
    if extension == '.mp3':
        meta = extraer_metadatos_mp3(ruta_completa)
    elif extension == '.m4a':
        meta = extraer_metadatos_m4a(ruta_completa)
    else:
        return None
    if not meta:
        return None
    meta['filename'] = os.path.basename(ruta_completa)
    meta['filepath'] = ruta_completa
    return meta

# === Función principal ===
def main(carpeta_musica, csv_salida, num_workers=4):
    campos_csv = [
        'filename', 'filepath', 'title', 'artist', 'album', 'album_artist',
        'genre', 'date', 'duration_seconds', 'bpm',
        'beaTunes_tempo_COLOR', 'beaTunes_SPECTRUM',
        'beaTunes_COLOR', 'beaTunes_tempo_timbre_COLOR',
        'MOOD_DANCEABILITY', 'Tuning', 'has_lyrics', 'lyrics_text'
    ]

    datos_canciones = []
    procesadas = 0
    ultimo_porcentaje = 0

    archivos = []
    for carpeta_raiz, _, files in os.walk(carpeta_musica):
        for archivo in files:
            ruta = os.path.join(carpeta_raiz, archivo)
            if os.path.splitext(archivo)[1].lower() in ('.mp3', '.m4a'):
                archivos.append(ruta)

    total = len(archivos)
    logging.info(f"Se encontraron {total} archivos para procesar.")

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futuros = {executor.submit(procesar_archivo, archivo): archivo for archivo in archivos}
        for futuro in as_completed(futuros):
            resultado = futuro.result()
            if resultado:
                datos_canciones.append(resultado)
            procesadas += 1
            
            porcentaje_actual = int((procesadas / total) * 100)
            
            # --- Barra de progreso interactiva en consola ---
            longitud_barra = 40
            relleno = int(longitud_barra * procesadas // total)
            barra = '=' * relleno + '-' * (longitud_barra - relleno)
            
            # --- Asignación de colores ANSI ---
            if porcentaje_actual < 50:
                color = "\033[93m"  # Amarillo claro
            elif porcentaje_actual < 100:
                color = "\033[94m"  # Azul claro
            else:
                color = "\033[92m"  # Verde claro
            reset = "\033[0m"       # Restaurar color original
            
            sys.stdout.write(f"\rProgreso: [{color}{barra}{reset}] {porcentaje_actual}% ({procesadas}/{total})")
            sys.stdout.flush()

            # --- Mensaje cada 10% únicamente en el archivo de log ---
            if porcentaje_actual >= ultimo_porcentaje + 10 or procesadas == total:
                mensaje = f"{porcentaje_actual}% completado ({procesadas}/{total})"
                logger = logging.getLogger()
                for handler in logger.handlers:
                    if isinstance(handler, logging.FileHandler):
                        record = logging.LogRecord(name=logger.name, level=logging.INFO, pathname=__file__, lineno=0, msg=mensaje, args=(), exc_info=None)
                        handler.emit(record)
                ultimo_porcentaje = porcentaje_actual

    sys.stdout.write("\n")

    with open(csv_salida, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=campos_csv)
        writer.writeheader()
        writer.writerows(datos_canciones)

    logging.info(f"Metadatos exportados a '{csv_salida}' con {len(datos_canciones)} canciones.")

# === Bloque principal ===
if __name__ == '__main__':
    multiprocessing.freeze_support()
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("musica_analisis.log", encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    import argparse

    parser = argparse.ArgumentParser(description="Extraer metadatos de archivos de música y exportar a CSV.")
    parser.add_argument("carpeta_musica", help="Ruta a la carpeta que contiene los archivos de música.")
    parser.add_argument("csv_salida", help="Ruta al archivo CSV de salida.")
    parser.add_argument("--threads", type=int, default=4, help="Número de hilos para procesamiento paralelo.")
    
    args = parser.parse_args()

    main(args.carpeta_musica, args.csv_salida, args.threads)