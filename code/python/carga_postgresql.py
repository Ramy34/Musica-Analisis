import os
from pathlib import Path
import pandas as pd
from datetime import datetime
import psycopg2
from io import StringIO

# === LIMPIAR NOMBRES DE COLUMNAS ===
def clean_name(name):
    """
    Limpia y normaliza nombres de columnas para Snowflake.
    """
    name = name.strip()
    # Reemplazar espacios, puntos, paréntesis y otros caracteres por _
    name = (
        name.replace(" ", "_")            
            .replace("(", "")
            .replace(")", "")
            .replace(".", "_")
            .replace("-", "_")
            .replace(":", "_")
            .replace("&", "_")
            .replace("/", "_")
            .replace("\\", "_")
            .replace("!", "")
            .replace("ö", "o")
            .replace("å", "a")
            .replace("á", "a")
            .replace("ú", "u")
            .replace("凛として時雨", "LING_TOSHITE_SHIGURE")
            .replace("ナノ", "NANO")
            .replace("フレデリック", "FREDERIC")
    )
    return name.upper()

def normaliza_fecha(fecha):
    if isinstance(fecha, str):
        fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
    return fecha.replace(microsecond=0)

# === TIPOS POSTGRES ===
def infer_postgres_type(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return "BIGINT"
    elif pd.api.types.is_float_dtype(dtype):
        return "DOUBLE PRECISION"
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return "TIMESTAMP"
    else:
        return "TEXT"

def lista_archivos_csv(ruta_carpeta):
    datos = []
    for carpeta, _, archivos_en_carpeta in os.walk(ruta_carpeta):
        for archivo in archivos_en_carpeta:
            ruta_completa = Path(carpeta) / archivo
            subcarpeta_relativa = os.path.relpath(carpeta, ruta_carpeta)
            fecha_modificacion = datetime.fromtimestamp(ruta_completa.stat().st_mtime)
            fecha_sf = fecha_modificacion.strftime("%Y-%m-%d %H:%M:%S")
            datos.append({
                'archivo': archivo,
                'ruta_completa': ruta_completa,
                'subcarpeta': subcarpeta_relativa.replace("\\", "_").upper(),
                "fecha_modificacion": normaliza_fecha(fecha_sf)
            })
    return datos

# === CONTROL PLAYLIST ===
def obtener_insertar(conn):
    cur = conn.cursor()
    cur.execute("SELECT name, schema_name, insertar, fecha_creacion_csv FROM adm.control_playlist")
    rows = cur.fetchall()
    cur.close()
    return [{"NAME": r[0], "SCHEMA_NAME": r[1], "INSERTAR": r[2], "FECHA_CREACION_CSV": r[3]} for r in rows]

def buscar_insertar(playlist_data, nombre, esquema, fecha_modificacion):
    for registro in playlist_data:
        if registro["NAME"] == nombre and registro["SCHEMA_NAME"] == esquema:
            if normaliza_fecha(registro["FECHA_CREACION_CSV"]) != fecha_modificacion:
                return registro["INSERTAR"]
            else:
                return False
    return None

def actualizar_control_playlist(flag, d, conn, nombre, esquema, registros):
    cur = conn.cursor()
    cur.execute("SET search_path TO adm;")

    if flag:
        cur.execute("""
            UPDATE adm.control_playlist
            SET records = %s,
                fecha_creacion_csv = %s,
                last_update_date = CURRENT_DATE
            WHERE name = %s AND schema_name = %s
        """, (registros, d['fecha_modificacion'], nombre, esquema))
    else:
        cur.execute("""
            INSERT INTO adm.control_playlist (name, schema_name, records, insertar, fecha_creacion_csv)
            VALUES (%s, %s, %s, TRUE, %s)
        """, (nombre, esquema, registros, d['fecha_modificacion']))

    conn.commit()
    cur.close()

def main(HOST, USER, PASSWORD, DB, CSV_PATH):
    # === CONEXIÓN A SNOWFLAKE ===
    conn = psycopg2.connect(
        host=HOST,
        database=DB,
        user=USER,
        password=PASSWORD
    )
    
    insertar = obtener_insertar(conn)

    for d in lista_archivos_csv(CSV_PATH):
        if d['archivo'].lower().endswith(".csv"):
            
            flag_insertar = buscar_insertar(insertar, clean_name(d['archivo'].replace(".csv", "")), d['subcarpeta'].upper(), d['fecha_modificacion'])

            if flag_insertar == False:
                print(f"[INFO] Omitido: {d['archivo']} en {d['subcarpeta']}")
            else:
                TABLE = clean_name(d['archivo'].replace(".csv", ""))
                SCHEMA = d['subcarpeta'].upper()
                # === CARGAR CSV CON PANDAS ===
                df = pd.read_csv(d['ruta_completa'])
                # Si el CSV está vacío, abortamos
                if df.empty:
                    print(f"[INFO] El archivo {d['archivo']} está vacío. Se omite.")
                    continue
                # Limpiar nombres de columnas
                df.columns = [clean_name(c) for c in df.columns]

                try:
                    cursor = conn.cursor()
                    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA};")
                    cols = ", ".join([f"{col} {infer_postgres_type(df[col].dtype)}" for col in df.columns])
                    cursor.execute(f"DROP TABLE IF EXISTS {SCHEMA}.{TABLE};")
                    create_table_sql = f"CREATE TABLE {SCHEMA}.{TABLE} ({cols});"
                    cursor.execute(create_table_sql)

                    # COPY (rápido)
                    buffer = StringIO()
                    df.to_csv(buffer, index=False, header=True)
                    buffer.seek(0)

                    cursor.copy_expert(f"COPY {SCHEMA}.{TABLE} FROM STDIN WITH CSV HEADER", buffer)

                    actualizar_control_playlist(flag_insertar, d, conn, TABLE, SCHEMA, len(df))
                except Exception as e:
                    print(f"[Error]: {e}")
                finally:
                    cursor.close()
        else:
            print(f"[INFO] Omitido (no es CSV): {d['archivo']}")
    conn.close()

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Cargar los CSV a Snowflake.")
    parser.add_argument("HOST", help="Host de POSTGRES.")
    parser.add_argument("USER", help="Usuario de POSTGRES.")
    parser.add_argument("PASSWORD", help="Contraseña de POSTGRES.")
    parser.add_argument("DATABASE", help="Base de datos de POSTGRES.")
    parser.add_argument("CSV_PATH", help="Ruta a la carpeta con los CSV.")
    
    args = parser.parse_args()

    main(args.HOST, args.USER, args.PASSWORD, args.DATABASE, args.CSV_PATH)