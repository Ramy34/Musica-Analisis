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

    print("\n✅ Proceso ETL completado con éxito.")

if __name__ == "__main__":
    main()
