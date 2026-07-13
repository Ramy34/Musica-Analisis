import json
import os
import platform
from pathlib import Path
from dotenv import load_dotenv

class Config:
    def __init__(self, config_path: str = "config/config.json"):
        self._config_path = Path(config_path)
        self._data = self._load_json()
        self._load_env()
        self._resolve_paths_by_os()

    def _load_json(self):
        with open(self._config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_env(self):
        load_dotenv()
        self.postgresql_credentials = {
            "host": os.getenv("POSTGRESQL_HOST"),
            "user": os.getenv("POSTGRESQL_USER"),
            "password": os.getenv("POSTGRESQL_PASSWORD"),
            "base": os.getenv("POSTGRESQL_DATABASE"),
            "port": os.getenv("POSTGRESQL_PORT")
        }
        
        # Carga el token de Genius desde tu archivo .env, o usa el json como respaldo
        self.api_keys = {
            "genius_token": os.getenv("GENIUS_TOKEN", self._data.get("api_keys", {}).get("genius_token"))
        }

    def _resolve_paths_by_os(self):
        system = platform.system()

        if system == "Windows":
            os_key = "windows"
        elif system == "Darwin":
            os_key = "macos"
        else:
            raise RuntimeError(f"OS no soportado: {system}")

        try:
            self._data["paths"] = {
                k: Path(v) for k, v in self._data["paths"][os_key].items()
            }
        except KeyError:
            raise KeyError(f"No existen paths definidos para OS: {os_key}")

    def get(self, section: str, key: str, default=None):
        return self._data.get(section, {}).get(key, default)

    def __getattr__(self, item):
        return self._data.get(item)
