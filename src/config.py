import json
from pathlib import Path

class Config:
    _instance = None
    _data: dict = {}
    CONFIG_PATH = Path.home() / ".jttconfig/config.json"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._load()
        return cls._instance
    
    def __bool__(self) -> bool:
        return bool(self._data)

    @classmethod
    def _load(cls):
        try:
            with open(cls.CONFIG_PATH, "r") as f:
                cls._data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            cls._data = {}  # Defaults to {}

    @classmethod
    def get(cls, key: str) -> str:
        value = cls._data.get(key)
        value = value if value else ""
        return value

    @classmethod
    def set(cls, key: str, value: str):
        cls._data[key] = value

    @classmethod
    def save(cls):
        cls.CONFIG_PATH.parent.mkdir(exist_ok=True, parents=True)
        with open(cls.CONFIG_PATH, "w") as f:
            json.dump(cls._data, f, indent=2)