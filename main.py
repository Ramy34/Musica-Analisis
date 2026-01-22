import multiprocessing
from config.config_loader import Config
from code.python import extraccion_metdatos, xml_to_csv, carga_snowflake, artistas, canciones_desnormalizadas, unir_csv

def main():
    config = Config()

    if config.general["procesar_todo"]:
        extraccion_metdatos.main(config.paths["music_folder"], config.paths["csv_metadata_output"], config.general["threads"], config.general["escala"])
    xml_to_csv.main(config.paths["input_folder"], config.paths["output_folder"])
    unir_csv.main(config.paths["csv_preraw"], config.paths["csv_raw"])
    artistas.main(config.paths["csv_metadata_output"], config.paths["csv_artistas_output"])
    canciones_desnormalizadas.main(config.paths["csv_metadata_output"], config.paths["csv_artistas_output"], config.paths["csv_canciones_output"])
    carga_snowflake.main(config.snowflake_credentials["account"], config.snowflake_credentials["user"], config.snowflake_credentials["password"], config.snowflake["warehouse"], config.snowflake["database"], config.paths["output_folder"])

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
