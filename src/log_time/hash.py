import hashlib
from pathlib import Path

def save(logs: list):
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent.parent
    file_path = root_dir / "data-hash-logs.log"
    with open(file_path, 'w') as file:
        for index, log in enumerate(logs):
            file.write(log)
            if not index == len(logs) - 1:
                file.write("\n")

def generate(data):
    logs: list = []
    for day, value in data.items():
        y, m, d = day
        for time, comment, issue in value:
            string_to_hash = f"{y}-{m}-{d}{time}{comment}{issue}"
            logs.append(hashlib.sha256(string_to_hash.encode()).hexdigest())

    return logs