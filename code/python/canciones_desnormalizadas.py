import pandas as pd

ruta_metadata = "D:/Códigos/Musica-Analisis/files/csv/RAW/Metadata.csv"
ruta_artista = "D:/Códigos/Musica-Analisis/files/csv/DW/Artistas.csv"
ruta_canciones = "D:/Códigos/Musica-Analisis/files/csv/DW/Canciones.csv"

def main(ruta_metadata, ruta_artista, ruta_canciones):
    # Cargar CSVs
    df_meta = pd.read_csv(ruta_metadata, low_memory=False)
    df_artista = pd.read_csv(ruta_artista, low_memory=False)

    # Join por artista
    join_cols = ['Artista'] 
    df_join1 = pd.merge(df_meta, df_artista, left_on=['artist'], right_on= ['Artista'], how='left')

    # Detectar filas sin match (por todas las columnas nuevas de itunes = NaN)
    columnas_artistas = [c for c in df_artista.columns if c not in join_cols]
    sin_match = df_join1[columnas_artistas].isnull().all(axis=1)

    # Combinar resultados finales:
    df_con_match = df_join1[~sin_match]
    df_final = df_con_match

    # Recalcular filas sin match finales (opcional)
    sin_match_final = df_final[columnas_artistas].isnull().all(axis=1)

    # Reemplazar columna 'Artista' con la homologada (si existe)
    df_final['Artista'] = df_final['Artista Homologado'].fillna(df_final['Artista'])

    # Eliminar columna 'Artista Homologado' para mantener estructura original
    df_final = df_final.drop(columns=['Artista Homologado'])

    print(f"[INFO] Total filas: {len(df_final)}")
    print(f"[INFO] Filas sin match finales: {sin_match_final.sum()}")

    # Guardar archivo final
    df_final.to_csv(ruta_canciones, index=False)
    print(f"[OK] Join final guardado en '{ruta_canciones}'")

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Desnormalizar canciones con datos de artistas.")
    parser.add_argument("RUTA_METADATA", help="Ruta al CSV de metadata.")
    parser.add_argument("RUTA_ARTISTA", help="Ruta al CSV de artistas.")
    parser.add_argument("RUTA_CANCIONES", help="Ruta al CSV de canciones desnormalizadas.")
    
    args = parser.parse_args()
    main(args.RUTA_METADATA, args.RUTA_ARTISTA, args.RUTA_CANCIONES)