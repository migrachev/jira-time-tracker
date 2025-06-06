from pathlib import Path
import hashlib

from .mytypes import UserData
from ..config import APP_DATA

def generate(data: UserData) -> list[str]:
    logs: list[str] = []
    
    for day, value in data.items():
        time: str; comment: str; issue: str
        y: int; m: int; d: int
        y, m, d = day
        for time, comment, issue in value:
            string_to_hash: str = f"{y}-{m}-{d}{time}{comment}{issue}"
            logs.append(hashlib.sha256(string_to_hash.encode()).hexdigest())

    return logs

def save(logs: list[str]):
    file_path: Path = APP_DATA / "data-hash-logs.log"
    with open(file_path, 'w') as file:
        index: int; log: str
        for index, log in enumerate(logs):
            file.write(log)
            if not index == len(logs) - 1:
                file.write("\n") 