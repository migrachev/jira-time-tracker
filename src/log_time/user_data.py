from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from typing import TextIO
from datetime import datetime, timedelta

from . import hash
from .utils import parse_iso_date, is_valid_date, split_work_log, in_conflict_with_previous_execution, is_valid_period
from .utils import are_proper_work_days, are_jira_identifiers_valid, are_times_valid, are_days_fully_logged
from .mytypes import UserData
from ..config import Config
from ..console import demand_choice, demand_period

def validate(user_data: UserData, period: tuple[str, str]):
    is_valid = True

    if not are_proper_work_days(user_data, period):
        print("\033[31mWeek days defined in the input data are improper!\033[0m")
        is_valid = False
    elif not are_jira_identifiers_valid(user_data):
        print("\033[31mJIRA identifier of the provided logs are missing or improper!\033[0m")
        is_valid = False
    elif not are_times_valid(user_data):
        print("\033[31mLog times provided in the data are missing or improper!\033[0m")
        is_valid = False
    elif not are_days_fully_logged(user_data):
        print("\033[31mThe days provided in the input data are not properly logged (8 hours per day)!\033[0m")
        is_valid = False
    else:
        logs_hash: list[str] = hash.generate(user_data)
        if in_conflict_with_previous_execution(logs_hash):
            print("\033[31mOne or more of the days provided in the input data have already been processed!\033[0m")
            is_valid = False

    return is_valid

def parse(string_data: str) -> UserData:
    parsed: UserData = {}
    work_day: tuple[int, int, int] = (0,0,0)

    lines = string_data.splitlines()
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        elif is_valid_date(stripped):
            work_day = parse_iso_date(stripped)
            parsed[work_day] = []
        else:
            work_log: tuple[str, str, str] = split_work_log(stripped)
            parsed[work_day].append(work_log)

    return parsed

def get_period() -> tuple[str, str]:
    title: str = "\033[34m\nWhat is the period you want to log in JIRA?\033[0m"
    label_start: str = "Enter the start of the period (yyyy-mm-dd)"
    label_end: str = "Enter the end of the period (yyyy-mm-dd)"
    invalid_date: str = "Your input is not a valid date. Make sure you provide date in yyyy-mm-dd format."
    invalid_period: str = "The period you entered is invalid. Note that period can't start or end on weekend day."
    
    start, end = demand_period(
        title=title,
        label_start=label_start,
        label_end=label_end,
        invalid_date=invalid_date,
        invalid_period=invalid_period,
        date_validator=is_valid_date,
        period_validator=is_valid_period,
        skip_clear=True
    )

    return start, end 

def get() -> tuple[tuple[str, str], str]:
    title: str = "\033[34mHow do you want to supply us with the data to process?\033[0m"
    options: dict[str, str] = {
        "file": "Refer data from file.",
        "paste": "Paste data as text."
    }
    choice: str = demand_choice(title, options)
    file_location: str = ""

    data: str = ""
    if choice == "paste":
        data = prompt("Paste your input here!")
        data = data.strip()
    else:
        default_logs_location = Config.get("default_logs_location")
        print()
        file_location = prompt(HTML("<ansiblue>Please provide the file location: </ansiblue>"), default=default_logs_location)
    
    start, end = get_period()

    if file_location:    
        with open(file_location, 'r', encoding='utf-8') as data_file:
            data_file: TextIO
            inside: bool = False
            actual_end = (datetime.fromisoformat(end) + timedelta(days=1)).isoformat().split("T")[0]

            for line in list(data_file):
                stripped: str = line.strip()
                is_comment = stripped.startswith("=") or stripped.startswith("#")
                is_empty = len(stripped) == 0

                if stripped == start:
                    inside = True
                elif stripped == actual_end:
                    inside = False

                if inside and not is_comment and not is_empty:
                    new_line = "\n"
                    if not data: new_line = ""
                    data += new_line + stripped

    return ((start, end), data)