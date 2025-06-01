import readchar
from prompt_toolkit import prompt
from typing import TextIO, Iterator

from . import hash
from .utils import parse_iso_date, is_valid_date, split_work_log, in_conflict_with_previous_execution
from .utils import is_proper_work_week, are_jira_identifiers_valid, are_times_valid, is_fully_logged_week
from .mytypes import UserData
from ..config import Config

def validate(user_data: UserData):
    is_valid = True

    if not is_proper_work_week(user_data):
        print("\033[31mWeek days defined in the input data are improper!\033[0m")
        is_valid = False
    elif not are_jira_identifiers_valid(user_data):
        print("\033[31mJIRA identifier of the provided logs are missing or improper!\033[0m")
        is_valid = False
    elif not are_times_valid(user_data):
        print("\033[31mLog times provided in the data are missing or improper!\033[0m")
        is_valid = False
    elif not is_fully_logged_week(user_data):
        print("\033[31mThe total sum of worked hours is not 40!\033[0m")
        is_valid = False
    else:
        logs_hash: list[str] = hash.generate(user_data)
        if in_conflict_with_previous_execution(logs_hash):
            print("\033[31mInput data have already been process!\033[0m")
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

def get() -> str:
    options: list[str] = [
        "Refer data from file.", 
        "Paste data as text."
    ]
    index: int = 0

    while True:
        print("How do you want to supply us with the data to process?\n")
        i: int; option: str
        for i, option in enumerate(options):
            if i == index:
                print(f"> \033[32m{option}\033[0m")  # Highlight the selected option
            else:
                print(f"  {option}")

        key: str = readchar.readkey() 

        if key == readchar.key.UP or key == readchar.key.LEFT:
            index = (index - 1) % len(options)
        elif key == readchar.key.DOWN or key == readchar.key.RIGHT:
            index = (index + 1) % len(options)
        elif key == readchar.key.ENTER or key == "\r":
            break  # Confirm selection

        print("\033c", end="")  # Clear screen

    data: str = ""
    if index:
        data = prompt("Paste your input here!")
        data = data.strip()
    else:
        default_file_location = Config.get("default_file_location")
        file_location: str = prompt("Please provide the file location: ", default=default_file_location)
        with open(file_location, 'r', encoding='utf-8') as data_file:
            data_file: TextIO
            flag: int = -1
            iterator: Iterator[str] = reversed(list(data_file))
            while flag < 1:
                line: str = next(iterator)
                stripped: str = line.strip()
                if stripped and (stripped.startswith("=") or stripped.startswith("#")):  # Comment/empty lines are ignored
                    if flag == 0:
                        flag = 1
                elif stripped:
                    flag = 0
                    new_line = "\n"
                    if not data: new_line = ""
                    data = stripped + new_line + data
    return data