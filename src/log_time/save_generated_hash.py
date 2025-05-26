from pathlib import Path

def saveGeneratedHash(logs: list[str]):
    scriptDir: Path = Path(__file__).parent
    rootDir: Path = scriptDir.parent.parent
    filePath: Path = rootDir / "data-hash-logs.log"
    with open(filePath, 'w') as file:
        index: int; log: str
        for index, log in enumerate(logs):
            file.write(log)
            if not index == len(logs) - 1:
                file.write("\n")