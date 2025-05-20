from pathlib import Path

def saveGeneratedHash(logs: list):
    scriptDir = Path(__file__).parent
    rootDir = scriptDir.parent.parent
    filePath = rootDir / "data-hash-logs.log"
    with open(filePath, 'w') as file:
        for index, log in enumerate(logs):
            file.write(log)
            if not index == len(logs) - 1:
                file.write("\n")