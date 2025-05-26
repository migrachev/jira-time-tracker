from utils import parseIsoDate, isValidDate, splitWorkLog
from mytypes import UserData

def parseUserData(stringData: str) -> UserData:
    parsed: UserData = {}
    workDay: tuple[int, int, int] = (0,0,0)

    lines = stringData.splitlines()
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        elif isValidDate(stripped):
            workDay = parseIsoDate(stripped)
            emptyValue: tuple[str, str, str] = ("", "", "")
            parsed[workDay] = emptyValue
        else:
            workLog: tuple[str, str, str] = splitWorkLog(stripped)
            parsed[workDay] = workLog

    return parsed