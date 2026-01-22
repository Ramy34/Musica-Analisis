import plistlib
import csv
import os
import urllib.parse
import sys

# Utilidades

def clean(name):
    if not name:
        return ""
    return (
        name.replace("＊", "*")
    )

def extract_filename_from_location(location):
    if not location:
        return ""
    decoded_path = urllib.parse.unquote(
        location.replace("file://localhost/", "")
    )
    return os.path.basename(decoded_path)

# Core: XML → filas
def parse_itunes_xml(input_file, rel_path):
    with open(input_file, "rb") as f:
        plist = plistlib.load(f)

    tracks = plist.get("Tracks", {})

    base_columns = [
        "Disliked", "Rating Computed", "Explicit", "Matched",
        "Compilation", "Sort Album Artist", "Purchased",
        "Sort Artist", "Sort Album", "Sort Name", "Composer",
        "Release Date", "Skip Date", "Skip Count", "Loved", 'Sort Composer'
    ]

    all_keys = set()
    for track_info in tracks.values():
        all_keys.update(track_info.keys())

    all_keys.update(base_columns)
    all_keys.update([
        "playlist",
        "carpeta_esquema",
        "ruta_absoluta",
        "filename"
    ])

    preferred_order = [
        "playlist",
        "carpeta_esquema",
        "ruta_absoluta",
        "filename",
        "Name",
        "Artist",
        "Album",
        "Genre",
        "Total Time"
    ]

    all_keys = sorted(all_keys, key=lambda x: (x not in preferred_order, x))

    playlist_name = os.path.splitext(os.path.basename(input_file))[0]
    carpeta_esquema = os.path.basename(rel_path) if rel_path != "." else ""
    ruta_absoluta = os.path.abspath(input_file)

    rows = []

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
                value = extract_filename_from_location(
                    track_info.get("Location", "")
                )
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

        rows.append(row)

    return all_keys, rows

# Escritura CSV
def write_csv(output_file, fieldnames, rows, append=False):
    mode = "a" if append else "w"
    write_header = not append or not os.path.exists(output_file)

    with open(output_file, mode, newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if write_header:
            writer.writeheader()

        writer.writerows(rows)

# Procesos
def process_raw(input_folder, output_folder):
    for root, _, files in os.walk(input_folder):
        for filename in files:
            if not filename.lower().endswith(".xml"):
                continue

            input_file = os.path.join(root, filename)
            rel_path = os.path.relpath(root, input_folder)

            output_subfolder = os.path.join(output_folder, rel_path)
            os.makedirs(output_subfolder, exist_ok=True)

            output_file = os.path.join(
                output_subfolder,
                filename.replace(".xml", ".csv")
            )

            fieldnames, rows = parse_itunes_xml(input_file, rel_path)
            write_csv(output_file, fieldnames, rows)

            print(f"[OK] Convertido: {filename}")

def process_pre_raw(input_folder, output_folder):
    all_rows = []
    fieldnames = None
    output_csv = os.path.join(output_folder, "Playlists.csv")

    for root, _, files in os.walk(input_folder):
        for filename in files:
            if not filename.lower().endswith(".xml"):
                continue

            input_file = os.path.join(root, filename)
            rel_path = os.path.relpath(root, input_folder)

            fn, rows = parse_itunes_xml(input_file, rel_path)

            if fieldnames is None:
                fieldnames = fn

            all_rows.extend(rows)

            print(f"[INFO] PRE_RAW -> Procesado: {filename}")

    if all_rows:
        write_csv(output_csv, fieldnames, all_rows)
        print(f"[OK] PRE_RAW unificado -> {output_csv}")
    else:
        print("[ADVERTENCIA] No se encontraron XML en PRE_RAW")

def main(input_folder, output_folder):
    raw_input = os.path.join(input_folder, "RAW")
    pre_raw_input = os.path.join(input_folder, "Pre_RAW")

    raw_output = os.path.join(output_folder, "RAW")


    if not os.path.isdir(raw_input):
        print(f"[ERROR] No existe: {raw_input}")
        return

    if not os.path.isdir(pre_raw_input):
        print(f"[ERROR] No existe: {pre_raw_input}")
        return

    os.makedirs(raw_output, exist_ok=True)

    process_raw(raw_input, raw_output)
    process_pre_raw(pre_raw_input, raw_output)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python xml_to_csv.py <carpeta_entrada> <carpeta_salida>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    main(input_folder, output_folder)