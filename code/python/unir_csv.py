import os
import pandas as pd


def main(carpeta_csv, ruta_csv_final):

    # Obtener todos los archivos CSV
    archivos_csv = [
        os.path.join(carpeta_csv, f)
        for f in os.listdir(carpeta_csv)
        if f.lower().endswith(".csv")
    ]

    # Validación
    if not archivos_csv:
        raise ValueError("No se encontraron archivos CSV en la carpeta")

    # Leer CSV uno por uno y agregar columna con el nombre del archivo
    dfs = []

    for archivo in archivos_csv:
        df = pd.read_csv(archivo)
        df["archivo_origen"] = os.path.basename(archivo)  # nueva columna
        dfs.append(df)

    # Unir todos los DataFrames
    df_final = pd.concat(dfs, ignore_index=True)

    # Guardar CSV final
    df_final.to_csv(ruta_csv_final, index=False, encoding="utf-8-sig")

    # Borrar los CSV originales
    for archivo in archivos_csv:
        os.remove(archivo)

    print("[OK] CSV unido correctamente y archivos originales eliminados")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Unir múltiples archivos CSV en uno solo.")
    parser.add_argument("carpeta_csv", help="Ruta a la carpeta que contiene los archivos CSV.")
    parser.add_argument("ruta_csv_final", help="Ruta donde se guardará el CSV final unido.")
    args = parser.parse_args()

    main(args.carpeta_csv, args.ruta_csv_final)
