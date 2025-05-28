import os
from pathlib import Path

# Rutas
carpeta_actual = Path(__file__).parent
carpeta_proyecto = carpeta_actual.parent
carpeta_proyecto = carpeta_proyecto / 'Archivos'

# Define la ruta de la carpeta que quieres limpiar
carpeta = Path(carpeta_proyecto)  # ← cambia esta ruta

# Verifica si existe la carpeta
if carpeta.exists() and carpeta.is_dir():
    archivos_eliminados = 0
    for archivo in carpeta.iterdir():
        if archivo.is_file():
            archivo.unlink()  # Elimina el archivo
            archivos_eliminados += 1
    print(f"[OK] Se eliminaron {archivos_eliminados} archivos en '{carpeta}'")
else:
    print(f"[ERROR] La carpeta '{carpeta}' no existe o no es una carpeta.")
