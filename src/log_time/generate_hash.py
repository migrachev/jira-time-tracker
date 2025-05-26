import hashlib
from mytypes import UserData

def generateHash(data: UserData) -> list[str]:
    logs: list[str] = []
    for day, value in data.items():
        time: str; comment: str; issue: str
        y: int; m: int; d: int
        y, m, d = day
        for time, comment, issue in value:
            stringToHash: str = f"{y}-{m}-{d}{time}{comment}{issue}"
            logs.append(hashlib.sha256(stringToHash.encode()).hexdigest())

    return logs