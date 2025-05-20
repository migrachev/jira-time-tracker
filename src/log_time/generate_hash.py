import hashlib

def generateHash(data):
    logs: list = []
    for day, value in data.items():
        y, m, d = day
        for time, comment, issue in value:
            stringToHash = f"{y}-{m}-{d}{time}{comment}{issue}"
            logs.append(hashlib.sha256(stringToHash.encode()).hexdigest())

    return logs