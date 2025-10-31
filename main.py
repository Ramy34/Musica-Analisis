import multiprocessing
from config.config_loader import Config
from code.python import extraccion_metdatos, xml_to_csv, carga_snowflake

def main():
    config = Config()

    #extraccion_metdatos.main(config.paths["music_folder"], config.paths["csv_metadata_output"], config.general["threads"], 1000)
    xml_to_csv.main(config.paths["input_folder"], config.paths["output_folder"])
    carga_snowflake.main(config.snowflake_credentials["account"], config.snowflake_credentials["user"], config.snowflake_credentials["password"], config.snowflake["warehouse"], config.snowflake["database"], config.paths["output_folder"])

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
