import plistlib
import csv
import os

def main(input_folder, output_folder):
    # Recorre todas las subcarpetas
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            if filename.lower().endswith(".xml"):
                input_file = os.path.join(root, filename)

                # Calcula la ruta relativa desde input_folder
                rel_path = os.path.relpath(root, input_folder)
                # Crea la misma subcarpeta dentro de output_folder
                output_subfolder = os.path.join(output_folder, rel_path)
                os.makedirs(output_subfolder, exist_ok=True)

                output_file = os.path.join(output_subfolder, filename.replace(".xml", ".csv"))

                with open(input_file, 'rb') as f:
                    plist = plistlib.load(f)

                tracks = plist.get("Tracks", {})

                # Obtiene todas las claves posibles de todos los tracks
                all_keys = set()
                for track_info in tracks.values():
                    all_keys.update(track_info.keys())

                # Agrega las nuevas columnas personalizadas
                all_keys.update(["playlist", "carpeta_esquema", "ruta_absoluta"])

                # Ordena columnas: primero las importantes si existen
                preferred_order = [
                    "playlist", "carpeta_esquema", "ruta_absoluta",
                    "Name", "Artist", "Album", "Genre", "Total Time"
                ]
                all_keys = sorted(all_keys, key=lambda x: (x not in preferred_order, x))

                # Determina los valores para las columnas nuevas
                playlist_name = os.path.splitext(filename)[0]
                carpeta_esquema = os.path.basename(rel_path) if rel_path != "." else ""
                ruta_absoluta = os.path.abspath(input_file)

                # Crea el CSV
                with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=all_keys)
                    writer.writeheader()

                    for track_info in tracks.values():
                        row = {}
                        for key in all_keys:
                            if key == "playlist":
                                value = playlist_name
                            elif key == "carpeta_esquema":
                                value = carpeta_esquema
                            elif key == "ruta_absoluta":
                                value = ruta_absoluta
                            else:
                                value = track_info.get(key, "")
                                # Convertir duración de ms a mm:ss
                                if key == "Total Time" and isinstance(value, int):
                                    minutes = value // 60000
                                    seconds = (value % 60000) // 1000
                                    value = f"{minutes}:{seconds:02d}"
                                elif isinstance(value, (dict, list)):
                                    value = str(value)  # Convertir dict/list a string
                            row[key] = value
                        writer.writerow(row)

                print(f"[INFO] Convertido: {input_file} → {output_file}")

    print("[OK] ¡Todos los XML se convirtieron a CSV manteniendo la estructura de carpetas!")

if __name__ == "__main__":

    import sys
    if len(sys.argv) != 3:
        print("Uso: python xml_to_csv.py <carpeta_entrada> <carpeta_salida>")
    else:
        input_folder = sys.argv[1]
        output_folder = sys.argv[2]
        main(input_folder, output_folder)