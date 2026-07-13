import os
import logging
from config.config_loader import Config
from code.python import insertar_letras

# Configuración básica de logs
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("musica_analisis_utilidades.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def main():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Iniciando el pipeline de Utilidades...")
        logging.info("Iniciando el pipeline de Utilidades...")
        
        # Cargamos la configuración general
        config = Config()

        print("Buscando e insertando letras de canciones en archivos de audio...")
        logging.info("Buscando e insertando letras de canciones en archivos de audio...")
        
        # Llamada al script de insertar letras pasando las credenciales de BD y el token
        # Asegúrate de tener "api_keys" y "genius_token" definidos en tu archivo config_loader.py
        insertar_letras.main(config.postgresql_credentials["host"], config.postgresql_credentials["user"], config.postgresql_credentials["password"], config.postgresql_credentials["base"], config.api_keys["genius_token"])
        
        print("El proceso finalizó con éxito.")
        logging.info("El proceso finalizó con éxito.")
    except Exception as e:
        print("Ocurrió un error. Revisa musica_analisis_utilidades.log para más detalles.")
        logging.error(f"Ocurrió un error en la ejecución: {e}", exc_info=True)

if __name__ == "__main__":
    main()