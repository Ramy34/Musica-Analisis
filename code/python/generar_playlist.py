import os

import psycopg2
from pathlib import Path
import sys
import logging

def clean(name):
    return (
        name.replace("_", " ").capitalize()
    )

def creacion_vistas(conn):
    # Ruta del script actual
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Construir ruta al SQL
    sql_path = os.path.join(base_dir, "..", "sql", "03 - Playlist.sql")

    cursor = conn.cursor()
    with open(sql_path, "r", encoding="utf-8") as f:
        sql = f.read()
    cursor.execute(sql)
    conn.commit()

    cursor.close()

def main(host, user, password, database, m3u_path):
    schema = "playlist"
    # === CONEXIÓN A POSTGRESQL ===
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    
    cur = conn.cursor()
    
    # === CREACIÓN DE VISTAS DE PLAYLISTS ===
    creacion_vistas(conn)

    # === OBTENER LISTA DE PLAYLISTS EXISTENTES ===
    lista_playlist_sql = f"SELECT table_name FROM information_schema.views WHERE table_schema = '{schema}';"
    cur.execute(lista_playlist_sql)
    rows = cur.fetchall()

    total = len(rows)
    if total == 0:
        logging.warning("No se encontraron playlists para generar.")
        return

    procesadas = 0

    for playlist in rows:
        playlist_name = playlist[0]
        logging.info(f"Procesando playlist: {clean(playlist_name)}")

        # === OBTENER CANCIONES DE LA PLAYLIST ===
        canciones_sql = f'SELECT "Artista", "Canción", "Ruta archivo" FROM {schema}."{playlist_name}" GROUP BY "Artista", "Canción", "Ruta archivo";'

        cur.execute(canciones_sql)
        canciones = cur.fetchall()

        # === GENERAR ARCHIVO M3U ===
        playlist_path = Path(m3u_path) / f"{clean(playlist_name)}.m3u8"

        with open(playlist_path, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for artista, cancion, ruta in canciones:
                f.write(f"#EXTINF:-1,{artista} - {cancion}\n")
                f.write(f"{ruta}\n")

        logging.info(f"Playlist generada: {playlist_path.resolve()} con {len(canciones)} canciones.")
        
        procesadas += 1
        porcentaje_actual = int((procesadas / total) * 100)
        
        longitud_barra = 40
        relleno = int(longitud_barra * procesadas // total)
        barra = '=' * relleno + '-' * (longitud_barra - relleno)
        
        color = "\033[93m" if porcentaje_actual < 50 else "\033[94m" if porcentaje_actual < 100 else "\033[92m"
        reset = "\033[0m"
        
        sys.stdout.write(f"\rProgreso Playlists: [{color}{barra}{reset}] {porcentaje_actual}% ({procesadas}/{total})")
        sys.stdout.flush()
   
    sys.stdout.write("\n")
    cur.close()
    conn.close()

if __name__ == "__main__":
    import argparse

    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )

    parser = argparse.ArgumentParser(description="Generar nuevas playlists.")
    parser.add_argument("HOST", help="Host de POSTGRES.")
    parser.add_argument("USER", help="Usuario de POSTGRES.")
    parser.add_argument("PASSWORD", help="Contraseña de POSTGRES.")
    parser.add_argument("DATABASE", help="Base de datos de POSTGRES.")
    parser.add_argument("M3U_PATH", help="Ruta a la carpeta con los archivos M3U.")
    
    args = parser.parse_args()

    main(args.HOST, args.USER, args.PASSWORD, args.DATABASE, args.M3U_PATH)