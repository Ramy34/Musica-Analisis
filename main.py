import multiprocessing
import os
import logging
from config.config_loader import Config
from code.python import carga_postgresql, extraccion_metdatos, xml_to_csv, generar_playlist

# Configuración básica de logs
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("musica_analisis.log", encoding='utf-8')
    ]
)

def main():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Iniciando el pipeline de Musica-Analisis...")
        logging.info("Iniciando el pipeline de Musica-Analisis...")
        config = Config()

        if config.general.get("procesar_todo", False):
            print("Ejecutando extracción de metadatos de archivos de audio...")
            logging.info("Ejecutando extracción de metadatos de archivos de audio...")
            extraccion_metdatos.main(config.paths["music_folder"], config.paths["csv_metadata_output"], config.general["threads"])
        
        print("Convirtiendo archivos XML a CSV...")
        logging.info("Convirtiendo archivos XML a CSV...")
        xml_to_csv.main(config.paths["input_folder"], config.paths["output_folder"])
        
        print("Cargando datos en la base de datos PostgreSQL...")
        logging.info("Cargando datos en la base de datos PostgreSQL...")
        carga_postgresql.main(config.postgresql_credentials["host"], config.postgresql_credentials["user"], config.postgresql_credentials["password"], config.postgresql_credentials["base"], config.paths["output_folder"])
        
        print("Generando playlists...")
        logging.info("Generando playlists...")
        generar_playlist.main(config.postgresql_credentials["host"], config.postgresql_credentials["user"], config.postgresql_credentials["password"], config.postgresql_credentials["base"], config.paths["m3u_playlist_output"])
        
        print("El proceso finalizó con éxito.")
        logging.info("El proceso finalizó con éxito.")
    except Exception as e:
        print("Ocurrió un error. Revisa musica_analisis.log para más detalles.")
        logging.error(f"Ocurrió un error en la ejecución: {e}", exc_info=True)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
