import psycopg2
from pathlib import Path

def clean(name):
    return (
        name.replace("_", " ").capitalize()
    )

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
    
    # === OBTENER LISTA DE PLAYLISTS EXISTENTES ===
    lista_playlist_sql = f"SELECT table_name FROM information_schema.views WHERE table_schema = '{schema}';"
    cur.execute(lista_playlist_sql)
    rows = cur.fetchall()

    for playlist in rows:
        playlist_name = playlist[0]
        print(f"[INFO] Procesando playlist: {clean(playlist_name)}")

        # === OBTENER CANCIONES DE LA PLAYLIST ===
        canciones_sql = f'SELECT "Artista original", "Canción", "Ruta archivo" FROM {schema}."{playlist_name}" GROUP BY "Artista original", "Canción", "Ruta archivo";'

        cur.execute(canciones_sql)
        canciones = cur.fetchall()

        # === GENERAR ARCHIVO M3U ===
        playlist_path = Path(m3u_path) / f"{clean(playlist_name)}.m3u8"

        with open(playlist_path, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for artista, cancion, ruta in canciones:
                f.write(f"#EXTINF:-1,{artista} - {cancion}\n")
                f.write(f"{ruta}\n")

        print(f"[OK] Playlist generada: {playlist_path.resolve()} con {len(canciones)} canciones.")
   
    cur.close()
    conn.close()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generar nuevas playlists.")
    parser.add_argument("HOST", help="Host de POSTGRES.")
    parser.add_argument("USER", help="Usuario de POSTGRES.")
    parser.add_argument("PASSWORD", help="Contraseña de POSTGRES.")
    parser.add_argument("DATABASE", help="Base de datos de POSTGRES.")
    parser.add_argument("M3U_PATH", help="Ruta a la carpeta con los archivos M3U.")
    
    args = parser.parse_args()

    main(args.HOST, args.USER, args.PASSWORD, args.DATABASE, args.M3U_PATH)