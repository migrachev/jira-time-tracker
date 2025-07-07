import re
import math
import threading
from datetime import datetime, timedelta
from typing import Callable

def debounce(func: Callable, snooze: float) -> Callable:
    timer = None

    def debounced(*args, **kwargs):
        nonlocal timer
        if timer:
            timer.cancel()
        timer = threading.Timer(snooze, lambda: func(*args, **kwargs))
        timer.start()

    return debounced

def get_calendar_date(date: str, offset: float = 0):
    dateobj = datetime.fromisoformat(date)
    dateobj += timedelta(minutes=offset)
    
    return dateobj.isoformat().split("T")[0]

def find_jira_id(subject: str) -> str:
    pattern = r'\b[A-Z][A-Z0-9_]{1,9}-\d+\b'
    match = re.search(pattern, subject)
    if match:
        return match.group(0)
    
    return ""

def remove_pattern_with_neighbors(name: str, pattern: str) -> str:
    # the regex matches non-space characters around the pattern
    regex = rf'\S*{re.escape(pattern)}\S*'
    result = re.sub(regex, '', name)
    return re.sub(r'\s+', ' ', result).strip()

def get_duration(start: str, end: str, roundup: bool = False) -> float:
    startobj = datetime.fromisoformat(start)
    endobj = datetime.fromisoformat(end)
    difference = endobj - startobj
    
    hours = difference.total_seconds() / 60 / 60
    if roundup:
        hours = math.ceil(hours * 2) / 2

    return hours

def events_overlap(event_one: dict, event_two: dict) -> bool:
    one_sdate = datetime.fromisoformat(event_one["startTime"])
    one_edate = datetime.fromisoformat(event_one["endTime"])
    two_sdate = datetime.fromisoformat(event_two["startTime"])
    two_edate = datetime.fromisoformat(event_two["endTime"])

    latest_start = max(one_sdate, two_sdate)
    earliest_end = min(one_edate, two_edate)

    return latest_start < earliest_end

def group_overlapping_events(events: list[dict]) -> list[list[dict]]:
    n = len(events)
    visited = [False] * n
    groups: list[list[dict]] = []

    def dfs(i: int, group: list[dict]):
        visited[i] = True
        group.append(events[i])
        for j in range(n):
            if not visited[j] and events_overlap(events[i], events[j]):
                dfs(j, group)

    for i in range(n):
        if not visited[i]:
            group: list[dict] = []
            dfs(i, group)
            groups.append(group)

    return groups