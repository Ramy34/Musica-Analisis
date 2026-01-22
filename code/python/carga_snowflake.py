import os
import snowflake.connector
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas

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

def infer_snowflake_type(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return "NUMBER"
    elif pd.api.types.is_float_dtype(dtype):
        return "FLOAT"
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return "TIMESTAMP_NTZ"
    else:
        return "STRING"

def lista_archivos_csv(ruta_carpeta):
    datos = []
    for carpeta, subcarpetas, archivos_en_carpeta in os.walk(ruta_carpeta):
        for archivo in archivos_en_carpeta:
            ruta_completa = os.path.join(carpeta, archivo)
            subcarpeta_relativa = os.path.relpath(carpeta, ruta_carpeta)
            datos.append({
                'archivo': archivo,
                'ruta_completa': ruta_completa,
                'subcarpeta': subcarpeta_relativa.replace("\\", "_").upper()
            })
    return datos

def obtener_insertar(conn):
    cur = conn.cursor()
    cur.execute(f"USE SCHEMA ADM;")
    # Traer todos los registros
    cur.execute("SELECT NAME, SCHEMA_NAME, INSERTAR FROM CONTROL_PLAYLIST")
    rows = cur.fetchall()
    # Convertir a lista de diccionarios
    playlist_data = [{"NAME": r[0], "SCHEMA_NAME": r[1], "INSERTAR": r[2]} for r in rows]
    cur.close()
    #conn.close()
    return playlist_data

def buscar_insertar(playlist_data, nombre, esquema):
    for registro in playlist_data:
        if registro["NAME"] == nombre and registro["SCHEMA_NAME"] == esquema:
            return registro["INSERTAR"]
    return None

def actualizar_control_playlist(insertar, d, conn, nombre, esquema, registros):
    cursor_tmp = conn.cursor()
    cursor_tmp.execute(f"USE SCHEMA ADM;")
    if buscar_insertar(insertar, clean_name(d['archivo'].replace(".csv", "")), d['subcarpeta'].upper()) == True:
        sql = f"UPDATE CONTROL_PLAYLIST SET RECORDS = {registros}, LAST_UPDATE_DATE = CURRENT_DATE WHERE NAME = '{nombre}' AND SCHEMA_NAME = '{esquema}';"
        cursor_tmp.execute(sql)        
    else:
        sql = f"INSERT INTO CONTROL_PLAYLIST (NAME, SCHEMA_NAME, RECORDS, INSERTAR) VALUES ('{nombre}', '{esquema}', {registros}, True)"
        cursor_tmp.execute(sql)
    conn.commit()
    print(f"[OK] Carga completada: {registros} filas insertadas en {esquema}.{nombre}")
    cursor_tmp.close()

def main(ACCOUNT, USER, PASSWORD, WAREHOUSE, DATABASE, CSV_PATH):
    # === CONEXIÓN A SNOWFLAKE ===
    conn = snowflake.connector.connect(
        user=USER,
        password=PASSWORD,
        account=ACCOUNT,
        warehouse=WAREHOUSE,
        database=DATABASE
    )

    insertar = obtener_insertar(conn)

    for d in lista_archivos_csv(CSV_PATH):
        if d['archivo'].lower().endswith(".csv"):

            if buscar_insertar(insertar, clean_name(d['archivo'].replace(".csv", "")), d['subcarpeta'].upper()) == False:
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
                    cursor.execute(f"USE SCHEMA {SCHEMA};")
                    cols = ", ".join([f"{col} {infer_snowflake_type(df[col].dtype)}" for col in df.columns])
                    #create_table_sql = f"CREATE TABLE IF NOT EXISTS {TABLE} ({cols});"
                    create_table_sql = f"CREATE OR REPLACE TABLE {TABLE} ({cols});"
                    cursor.execute(create_table_sql)

                    success, nchunks, nrows, _ = write_pandas(
                    conn,
                    df,
                    TABLE,
                    auto_create_table=False,
                    overwrite=True
                    )
                    actualizar_control_playlist(insertar, d, conn, TABLE, SCHEMA, nrows)
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
    parser.add_argument("ACCOUNT", help="Cuenta de snowflake.")
    parser.add_argument("USER", help="Usuario de snowflake.")
    parser.add_argument("PASSWORD", help="Contraseña de snowflake.")
    parser.add_argument("WAREHOUSE", help="Warehouse de snowflake.")
    parser.add_argument("DATABASE", help="Base de datos de snowflake.")
    parser.add_argument("CSV_PATH", help="Ruta a la carpeta con los CSV.")
    
    args = parser.parse_args()

    main(args.ACCOUNT, args.USER, args.PASSWORD, args.WAREHOUSE, args.DATABASE, args.CSV_PATH)