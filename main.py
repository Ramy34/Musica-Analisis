import multiprocessing
from config.config_loader import Config
from code.python import carga_postgresql, extraccion_metdatos, xml_to_csv

def main():
    config = Config()

    if config.general["procesar_todo"]:
        extraccion_metdatos.main(config.paths["music_folder"], config.paths["csv_metadata_output"], config.general["threads"])
    xml_to_csv.main(config.paths["input_folder"], config.paths["output_folder"])
    carga_postgresql.main(config.postgresql_credentials["host"], config.postgresql_credentials["user"], config.postgresql_credentials["password"], config.postgresql_credentials["base"], config.paths["output_folder"])

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
