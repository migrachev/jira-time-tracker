import readchar
from prompt_toolkit import prompt
from typing import TextIO, Iterator
from utils import parse_iso_date, is_valid_date, split_work_log, in_conflict_with_previous_execution
from utils import is_proper_work_week, are_jira_identifiers_valid, are_times_valid, is_fully_logged_week
from mytypes import UserData

def validate(user_data: UserData, logs_hash: list[str]):
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
    elif in_conflict_with_previous_execution(logs_hash):
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
            empty_value: tuple[str, str, str] = ("", "", "")
            parsed[work_day] = empty_value
        else:
            work_log: tuple[str, str, str] = split_work_log(stripped)
            parsed[work_day] = work_log

    return parsed

def get(default_file_location: str) -> str:
    options: list[str] = [
        "Refer data from file.", 
        "Paste data as text."
    ]
    index: int = 0  # Start at the first option

    while True:
        print("How do you want to supply us with the data to process?\n")
        # Display options
        i: int; option: str
        for i, option in enumerate(options):
            if i == index:
                print(f"> \033[32m{option}\033[0m")  # Highlight the selected option
            else:
                print(f"  {option}")

        key: str = readchar.readkey()  # Wait for key press

        if key == readchar.key.UP or key == readchar.key.LEFT:
            index = (index - 1) % len(options)  # Move selection up/left
        elif key == readchar.key.DOWN or key == readchar.key.RIGHT:
            index = (index + 1) % len(options)  # Move selection down/right
        elif key == readchar.key.ENTER or key == "\r":
            break  # Confirm selection

        print("\033c", end="")  # Clear screen

    data: str = ""
    if index:
        data = prompt("Paste your input here!")
    else:
        file_location: str = prompt("Please provide the file location: ", default=default_file_location)
        with open(file_location, 'r', encoding='utf-8') as data_file:
            data_file: TextIO
            flag: int = -1
            iterator: Iterator[str] = reversed(list(data_file))
            while flag < 1:
                line: str = next(iterator)
                stripped: str = line.strip()
                if stripped and (line.startswith("=") or line.startswith("#")):  # comment/empty lines ignored
                    if flag == 0:
                        flag = 1
                elif stripped:
                    flag = 0
                    data = line + data
    return data