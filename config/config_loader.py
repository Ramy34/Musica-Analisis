import json
import os
from pathlib import Path
from dotenv import load_dotenv

class Config:
    def __init__(self, config_path: str = "config/config.json"):
        self._config_path = Path(config_path)
        self._data = self._load_json()
        self._load_env()

    def _load_json(self):
        with open(self._config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_env(self):
        load_dotenv()
        self.snowflake_credentials = {
            "account": os.getenv("SNOWFLAKE_ACCOUNT"),
            "user": os.getenv("SNOWFLAKE_USER"),
            "password": os.getenv("SNOWFLAKE_PASSWORD")
        }

    def get(self, section: str, key: str, default=None):
        return self._data.get(section, {}).get(key, default)

    def __getattr__(self, item):
        return self._data.get(item)
