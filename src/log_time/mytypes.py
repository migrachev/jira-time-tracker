from typing import TypedDict

class WorkLog(TypedDict):
    started: str
    comment: str
    timeSpentSeconds: float

class WorkLogRequest(TypedDict):
    url: str
    body: WorkLog

UserData = dict[tuple[int, int, int], tuple[str, str, str]]
