import json
import os

class AppConfig:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config_path="code/config/appsettings.json"):
        if self._initialized:
            return
        self.config_path = config_path
        self.settings = {}
        self.load_config()
        self._initialized = True

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self.settings = json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
        else:
            print(f"Config file not found: {self.config_path}")

    def get(self, key, default=None):
        keys = key.split(".")
        data = self.settings
        for k in keys:
            if isinstance(data, dict) and k in data:
                data = data[k]
            else:
                return default
        return data if data is not None else default
    