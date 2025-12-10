import plistlib
import csv
import os
import urllib.parse

def clean(name):
    name = (
        name.replace("＊", "*")
        .replace("＊", "*")
    )
    return name

def extract_filename_from_location(location):
    if not location:
        return ""
    # Quita el prefijo "file://localhost/" y decodifica caracteres especiales (%20, %C3%A9, etc.)
    decoded_path = urllib.parse.unquote(location.replace("file://localhost/", ""))
    # Extrae solo el nombre del archivo
    return os.path.basename(decoded_path)

def main(input_folder, output_folder):
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            if filename.lower().endswith(".xml"):
                input_file = os.path.join(root, filename)

                rel_path = os.path.relpath(root, input_folder)
                output_subfolder = os.path.join(output_folder, rel_path)
                os.makedirs(output_subfolder, exist_ok=True)

                output_file = os.path.join(output_subfolder, filename.replace(".xml", ".csv"))

                with open(input_file, 'rb') as f:
                    plist = plistlib.load(f)

                tracks = plist.get("Tracks", {})

                colums = ["Disliked", "Rating Computed", "Explicit", "Matched", "Compilation", "Sort Album Artist", "Purchased", 
                          "Sort Artist", "Sort Album" ,"Sort Name", "Composer", "Release Date", "Skip Date", "Skip Count"
                          ]      
                all_keys = set()
                for track_info in tracks.values():
                    for colum in colums:
                        if track_info.keys() == colum:
                            colums.remove(colum)
                    all_keys.update(track_info.keys())

                all_keys.update(colums) 
                # Nuevas columnas personalizadas
                all_keys.update(["playlist", "carpeta_esquema", "ruta_absoluta", "filename"])

                preferred_order = [
                    "playlist", "carpeta_esquema", "ruta_absoluta", "filename",
                    "Name", "Artist", "Album", "Genre", "Total Time"
                ]
                all_keys = sorted(all_keys, key=lambda x: (x not in preferred_order, x))

                playlist_name = os.path.splitext(filename)[0]
                carpeta_esquema = os.path.basename(rel_path) if rel_path != "." else ""
                ruta_absoluta = os.path.abspath(input_file)

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
                            elif key == "filename":
                                value = extract_filename_from_location(track_info.get("Location", ""))
                            elif key == "Artist":
                                value = clean(track_info.get("Artist", "Unknown Artist"))                                           
                            else:
                                value = track_info.get(key, "")
                                if key == "Total Time" and isinstance(value, int):
                                    minutes = value // 60000
                                    seconds = (value % 60000) // 1000
                                    value = f"{minutes}:{seconds:02d}"
                                elif isinstance(value, (dict, list)):
                                    value = str(value)
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
