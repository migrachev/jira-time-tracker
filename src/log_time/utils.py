import re
import itertools
import sys
import time
import threading
from datetime import datetime
from pathlib import Path


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
    
def split_work_log(s: str):
    if s.startswith('-'):
        s = s[1:]
    s = s.strip()
    
    first_space_index = s.find(' ')
    last_space_index = s.rfind(' ')
    
    if first_space_index == -1:
        return s, '', ''
    
    first_part = s[:first_space_index]
    second_part = s[first_space_index + 1:last_space_index] if last_space_index != first_space_index else ''
    third_part = s[last_space_index + 1:]
    
    return first_part, second_part, third_part

def is_proper_work_week(data: dict):
    dates: list = data.keys()
    date_objects = [datetime(year=y, month=m, day=d) for (y, m, d) in dates]
    first_week = date_objects[0].isocalendar()[1]
    working_days = set()

    for date in date_objects:
        if date.weekday() < 5:
            if date.isocalendar()[1] != first_week:
                return False
            working_days.add(date.weekday())
    
    return len(working_days) == 5

def are_jira_identifiers_valid(data: dict) -> bool:
    result = True
    pattern = r'^[A-Z]{1,10}-\d+$'

    issues: list = []
    for _, value in data.items():
        for _, _, issue in value:
            issues.append(issue)


    for issue in issues:
        if not re.match(pattern, issue):
            result = False

    return result

def are_times_valid(data: dict) -> bool:
    result = True

    times: list = []
    for _, value in data.items():
        for time, _, _ in value:
            times.append(time)

    for time in times:
        if not time.endswith('h'):
            result = False
            break

        time_str = time[:-1]
        if not re.match(r'^\d+(\.5)?$', time_str):
            result = False
            break

        time_value = float(time_str)
        if time_value <= 0 or time_value > 8:
            result = False
            break

    return result

def is_fully_logged_week(data: dict): #expects already checked data with areTimesValid
    total: float = 0
    for _, value in data.items():
        for time, _, _ in value:
            total = total + float(time[:-1])

    return total == 40
    
def is_in_conflict_with_previous_execution(logs: list) -> bool:
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent.parent
    file_path = root_dir / "data-hash-logs.log"
    with open(file_path, "r") as logs_file:
        result = False
        for line in list(logs_file):
            if line in logs:
                result = True
        return result
    
def spinner(loading_event):
    for symbol in itertools.cycle(["Processing |", "Processing /", "Processing -", "Processing \\"]):
        if loading_event.is_set():
            break
        sys.stdout.write(f"\r{symbol}")
        sys.stdout.flush()
        time.sleep(0.2)  #Speed of rotation

def start_spinner_thread(loading_event):
    spinner_thread = threading.Thread(target=spinner, args=(loading_event,), daemon=True)
    spinner_thread.start()