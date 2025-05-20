from utils import parseIsoDate, isValidDate, splitWorkLog

def parseUserData(stringData):
    parsed: dict = {}
    workDay: tuple = (0,0,0)

    lines = stringData.splitlines()
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        elif isValidDate(stripped):
            workDay = parseIsoDate(stripped)
            parsed[workDay] = []
        else:
            workLog = splitWorkLog(stripped)
            parsed[workDay].append(workLog)

    return parsed