from pathlib import Path
import subprocess
import sys


def ejecutar_script(ruta):
    print(f"\n▶ Ejecutando: {ruta}")
    try:
        process = subprocess.Popen(
            ['python', '-u', ruta],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in process.stdout:
            print(line, end='')

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

     # 🧪 Validar si hay archivos XML antes de continuar
    carpeta_entrada = Path('Archivos')  # Ajusta esta ruta si es diferente
    archivos_xml = list(carpeta_entrada.glob("*.xml"))

    if not archivos_xml:
        print("\n🛑 No se encontraron archivos XML en la carpeta 'Entrada'. Proceso detenido.")
        sys.exit(1)
    
    print(f"📂 Se encontraron {len(archivos_xml)} archivo(s) XML. Iniciando proceso ETL...")

    print("\n1) Extracción de datos")
    if not ejecutar_script('Programas/extraccion.py'):
        print("🛑 Proceso detenido por error en extracción.")
        sys.exit(1)

    print("\n2) Conversión de datos")
    if not ejecutar_script('Programas/convertidor.py'):
        print("🛑 Proceso detenido por error en conversión.")
        sys.exit(1)

    print("\n3) Unión de datos")
    if not ejecutar_script('Programas/join.py'):
        print("🛑 Proceso detenido por error en unión.")
        sys.exit(1)

    print("\n4) Filtrado de columnas")
    if not ejecutar_script('Programas/filtrado.py'):
        print("🛑 Proceso detenido por error en el filtrado.")
        sys.exit(1)

    print("\n5) Creación del resúmen general")
    if not ejecutar_script('Programas/resumen_general.py'):
        print("🛑 Proceso detenido por error en la creación del resúmen general.")
        sys.exit(1)

    print("\n6) Actualización del catálogo de artistas")
    if not ejecutar_script('Programas/actualizar_artistas.py'):
        print("🛑 Proceso detenido por error en la actualización del catalogo de artistas.")
        sys.exit(1)
    
    print("\n7) Generar lista de canciones desnormalizada")
    if not ejecutar_script('Programas/canciones.py'):
        print("🛑 Proceso detenido por error en la desnormalización de canciones.")
        sys.exit(1)

    print("\n8) Borrado de archivos de entrada")
    if not ejecutar_script('Programas/borrado.py'):
        print("🛑 Proceso detenido por error en el borrado.")
        sys.exit(1)        

    print("\n✅ Proceso ETL completado con éxito.")

if __name__ == "__main__":
    main()
