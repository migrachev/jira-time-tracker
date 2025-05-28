import re
import itertools
import sys
import time
import threading
from datetime import datetime
from pathlib import Path
from typing import KeysView
from threading import Event
from .mytypes import UserData

def parse_iso_date(date_str: str) -> tuple[int, int, int]:
    year, month, day = map(int, date_str.split("-"))
    return year, month, day

def is_valid_date(date_str: str) -> bool:
    try:
        date_str = '-'.join([str(int(part)) for part in date_str.split('-')])
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    
def split_work_log(s: str) -> tuple[str, str, str]:
    s = s.strip()
    if s.startswith('-'):
        s = s[1:]
    s = s.strip()
    
    first_space_index: int = s.find(' ')
    last_space_index: int = s.rfind(' ')
    
    if first_space_index == -1:
        return s, '', ''
    
    first_part: str = s[:first_space_index]
    second_part: str = s[first_space_index + 1:last_space_index] if last_space_index != first_space_index else ''
    third_part: str = s[last_space_index + 1:]
    
    return first_part.strip(), second_part.strip(), third_part.strip()

def is_proper_work_week(data: UserData) -> bool:
    dates: KeysView = data.keys()
    date_objects: list[datetime] = [datetime(year=y, month=m, day=d) for (y, m, d) in dates]
    first_week: int = date_objects[0].isocalendar()[1]
    working_days: set = set()

    for date in date_objects:
        if date.weekday() < 5:
            if date.isocalendar()[1] != first_week:
                return False
            working_days.add(date.weekday())
    
    return len(working_days) == 5

def are_jira_identifiers_valid(data: UserData) -> bool:
    result: bool = True
    pattern = r'^[A-Z]{1,10}-\d+$'

    issues: list = []; value: list[tuple[str, str, str]]
    for _, value in data.items():
        issue: str
        for _, _, issue in value:
            issues.append(issue)

    for issue in issues:
        issue: str
        if not re.match(pattern, issue):
            result = False

    return result

def are_times_valid(data: UserData) -> bool:
    result: bool = True

    times: list = []; value: list[tuple[str, str, str]]
    for _, value in data.items():
        time: str
        for time, _, _ in value:
            times.append(time)

    for time in times:
        time: str
        if not time.endswith('h'):
            result = False
            break

        time = time[:-1]
        if not re.match(r'^\d+(\.5)?$', time):
            result = False
            break

        time_value = float(time)
        if time_value <= 0 or time_value > 8:
            result = False
            break

    return result

def is_fully_logged_week(data: UserData): #expects already checked data with are_times_valid
    total: float = 0; value: list[tuple[str, str, str]]
    for _, value in data.items():
        time: str
        for time, _, _ in value:
            total += float(time[:-1])

    return total == 40
    
def in_conflict_with_previous_execution(logs: list[str]) -> bool:
    script_dir: Path = Path(__file__).parent
    root_dir: Path = script_dir.parent.parent
    file_path: Path = root_dir / "data-hash-logs.log"
    with open(file_path, "r") as logs_file:
        result = False
        for line in list(logs_file):
            print(line)
            if line in logs:
                result = True
        return result
    
def spinner(loading_event: Event):
    for symbol in itertools.cycle(["Processing |", "Processing /", "Processing -", "Processing \\"]):
        if loading_event.is_set():
            break
        sys.stdout.write(f"\r{symbol}")
        sys.stdout.flush()
        time.sleep(0.2)  #Speed of rotation

def start_spinner_thread(loading_event: Event):
    spinner_thread = threading.Thread(target=spinner, args=(loading_event,), daemon=True)
    spinner_thread.start()