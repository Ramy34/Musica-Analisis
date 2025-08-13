from pathlib import Path
import subprocess
import sys
import os

def ejecutar_script(ruta):
    print(f"\n▶ Ejecutando: {ruta}")
    try:

        process = subprocess.Popen(
            ['python', '-u', ruta],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        for line in process.stdout:
            print(line, end='')  # Mostramos tal cual, para respetar \r

        process.wait()

        if process.returncode != 0:
            print(f"\n❌ El script {ruta} falló con código {process.returncode}.")
            return False

        return True

    except FileNotFoundError:
        print(f"\n❌ No se encontró el script: {ruta}")
        return False
    except Exception as e:
        print(f"\n❌ Error al ejecutar {ruta}: {e}")
        return False

def main():
    print("🚀 Proceso de extracción, transformación y carga de datos")

    carpeta_entrada = Path('Archivos')
    archivos_xml = list(carpeta_entrada.glob("*.xml"))

    if not archivos_xml:
        print("\n🛑 No se encontraron archivos XML en la carpeta 'Entrada'. Proceso detenido.")
        sys.exit(1)

    print(f"📂 Se encontraron {len(archivos_xml)} archivo(s) XML. Iniciando proceso ETL...")

    if not ejecutar_script('Programas/extraccion.py'):
        print("🛑 Proceso detenido por error en extracción.")
        sys.exit(1)

    if not ejecutar_script('Programas/convertidor.py'):
        print("🛑 Proceso detenido por error en conversión.")
        sys.exit(1)

    if not ejecutar_script('Programas/join.py'):
        print("🛑 Proceso detenido por error en unión.")
        sys.exit(1)

    if not ejecutar_script('Programas/filtrado.py'):
        print("🛑 Proceso detenido por error en el filtrado.")
        sys.exit(1)

    if not ejecutar_script('Programas/resumen_general.py'):
        print("🛑 Proceso detenido por error en la creación del resúmen general.")
        sys.exit(1)

    if not ejecutar_script('Programas/actualizar_artistas.py'):
        print("🛑 Proceso detenido por error en la actualización del catalogo de artistas.")
        sys.exit(1)

    if not ejecutar_script('Programas/canciones.py'):
        print("🛑 Proceso detenido por error en la desnormalización de canciones.")
        sys.exit(1)

    if not ejecutar_script('Programas/playlist.py'):
        print("🛑 Proceso detenido por error en la creación del reporte de playlist.")
        sys.exit(1)

    if not ejecutar_script('Programas/borrado.py'):
        print("🛑 Proceso detenido por error en el borrado.")
        sys.exit(1)

    print("\n✅ Proceso ETL completado con éxito.")

if __name__ == "__main__":
    main()
