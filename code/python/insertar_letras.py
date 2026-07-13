import os
import logging
import sys
import psycopg2
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.id3 import ID3, USLT
import lyricsgenius

# Configuración básica de logs
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("musica_analisis_utilidades.log", encoding='utf-8')
    ]
)

def insertar_letra_mp3(ruta, letra):
    try:
        audio = MP3(ruta)
        if audio.tags is None:
            audio.add_tags()
        
        # Eliminar letras anteriores si existen (por limpieza)
        audio.tags.delall('USLT')
        
        # Insertar nueva letra (encoding=3 es UTF-8)
        audio.tags.add(USLT(encoding=3, lang='eng', desc='', text=letra))
        audio.save()
        return True
    except Exception as e:
        logging.error(f"Error al insertar letra en MP3 {ruta}: {e}")
        return False

def insertar_letra_m4a(ruta, letra):
    try:
        audio = MP4(ruta)
        if audio.tags is None:
            audio.add_tags()
        
        # Guardar la letra en el átomo de lyrics estándar de Apple
        audio.tags['©lyr'] = [letra]
        audio.save()
        return True
    except Exception as e:
        logging.error(f"Error al insertar letra en M4A {ruta}: {e}")
        return False

def obtener_metadatos(ruta, extension):
    try:
        if extension == '.mp3':
            audio = MP3(ruta)
            tags = audio.tags or {}
            titulo = tags.get('TIT2', [''])[0] if 'TIT2' in tags else ''
            artista = tags.get('TPE1', [''])[0] if 'TPE1' in tags else ''
            return str(titulo), str(artista), tags
        elif extension == '.m4a':
            audio = MP4(ruta)
            tags = audio.tags or {}
            titulo = tags.get('\xa9nam', [''])[0] if '\xa9nam' in tags else ''
            artista = tags.get('\xa9ART', [''])[0] if '\xa9ART' in tags else ''
            return str(titulo), str(artista), tags
    except Exception as e:
        logging.debug(f"Error al leer metadatos de {ruta}: {e}")
    return '', '', None

def main(host, user, password, database, genius_token):
    # Inicializamos el cliente de Genius
    genius = lyricsgenius.Genius(genius_token)
    genius.verbose = False
    genius.remove_section_headers = True
    
    try:
        # Conectarse a PostgreSQL
        conn = psycopg2.connect(host=host, user=user, password=password, database=database)
        cur = conn.cursor()
        
        # Consultar la base de datos por las canciones que nos interesan
        query = """
            SELECT "Ruta archivo" 
            FROM vista.biblioteca 
            WHERE "Me gusta" = 'Sí' AND "Tiene letra" = 'No';
        """
        cur.execute(query)
        archivos = [row[0] for row in cur.fetchall()]
        
        cur.close()
        conn.close()
    except Exception as e:
        logging.error(f"Error al conectar con la base de datos: {e}")
        return
                
    total = len(archivos)
    if total == 0:
        logging.info("No se encontraron canciones favoritas sin letra en la base de datos.")
        return
        
    logging.info(f"Se encontraron {total} canciones pendientes por buscar letra.")
    
    procesadas = 0
    actualizadas = 0
    
    for ruta in archivos:
        if not os.path.exists(ruta):
            logging.warning(f"El archivo ya no existe en la ruta especificada: {ruta}")
        else:
            extension = os.path.splitext(ruta)[1].lower()
            titulo, artista, tags = obtener_metadatos(ruta, extension)
            
            if not titulo or not artista:
                logging.warning(f"Faltan metadatos de artista o título en: {os.path.basename(ruta)}")
            else:
                logging.info(f"Buscando letra para: {titulo} - {artista}")
                try:
                    cancion = genius.search_song(titulo, artista)
                    if cancion and cancion.lyrics:
                        letra = cancion.lyrics
                        if letra.endswith('Embed'):
                            letra = letra[:-5]
                        exito = insertar_letra_mp3(ruta, letra) if extension == '.mp3' else insertar_letra_m4a(ruta, letra)
                        if exito:
                            logging.info(f"¡Letra guardada en el archivo {os.path.basename(ruta)}!")
                            actualizadas += 1
                    else:
                        logging.info(f"No se encontró la letra para: {titulo} - {artista}")
                except Exception as e:
                    logging.error(f"Error al buscar la letra de {titulo} - {artista}: {e}")
                
        procesadas += 1
        porcentaje_actual = int((procesadas / total) * 100)
        
        longitud_barra = 40
        relleno = int(longitud_barra * procesadas // total)
        barra = '=' * relleno + '-' * (longitud_barra - relleno)
        
        color = "\033[93m" if porcentaje_actual < 50 else "\033[94m" if porcentaje_actual < 100 else "\033[92m"
        reset = "\033[0m"
        
        sys.stdout.write(f"\rProgreso Letras: [{color}{barra}{reset}] {porcentaje_actual}% ({procesadas}/{total})")
        sys.stdout.flush()

    sys.stdout.write("\n")

    logging.info(f"Proceso finalizado. Se incrustó la letra a {actualizadas} de {total} canciones.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Buscar e insertar letras basándose en la DB.")
    parser.add_argument("host", help="Host de POSTGRES.")
    parser.add_argument("user", help="Usuario de POSTGRES.")
    parser.add_argument("password", help="Contraseña de POSTGRES.")
    parser.add_argument("database", help="Base de datos de POSTGRES.")
    parser.add_argument("genius_token", help="Token de acceso de la API de Genius.")
    
    args = parser.parse_args()
    main(args.host, args.user, args.password, args.database, args.genius_token)