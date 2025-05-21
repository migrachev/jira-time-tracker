import readchar
from prompt_toolkit import prompt
from utils import parse_iso_date, is_valid_date, split_work_log, is_in_conflict_with_previous_execution
from utils import is_proper_work_week, are_jira_identifiers_valid, are_times_valid, is_fully_logged_week

def validate_data(user_data: dict, logs_hash: list):
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
    elif is_in_conflict_with_previous_execution(logs_hash):
        print("\033[31mInput data have already been process!\033[0m")
        is_valid = False

    return is_valid


def parse_data(string_data):
    parsed: dict = {}
    work_day: tuple = (0,0,0)

    lines = string_data.splitlines()
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        elif is_valid_date(stripped):
            work_day = parse_iso_date(stripped)
            parsed[work_day] = []
        else:
            work_log = split_work_log(stripped)
            parsed[work_day].append(work_log)

    return parsed

def get_data(default_file_location):
    options = [
        "Refer data from file.", 
        "Paste data as text."
    ]
    index = 0  # Start at the first option

    while True:
        print("How do you want to supply us with the data to process?\n")
        # Display options
        for i, option in enumerate(options):
            if i == index:
                print(f"> \033[32m{option}\033[0m")  # Highlight the selected option
            else:
                print(f"  {option}")

        key = readchar.readkey()  # Wait for key press

        if key == readchar.key.UP or key == readchar.key.LEFT:
            index = (index - 1) % len(options)  # Move selection up/left
        elif key == readchar.key.DOWN or key == readchar.key.RIGHT:
            index = (index + 1) % len(options)  # Move selection down/right
        elif key == readchar.key.ENTER or key == "\r":
            break  # Confirm selection with Enter

        print("\033c", end="")  # Clear screen for smooth UI update

    data = ""
    if index:
        data = prompt("Paste your input here!")
    else:
        file_location = prompt("Please provide the file location: ", default=default_file_location)
        with open(file_location, 'r', encoding='utf-8') as data_file:
            flag: int = -1
            iterator = reversed(list(data_file))
            while flag < 1:
                line = next(iterator)
                stripped = line.strip()
                if stripped and (line.startswith("=") or line.startswith("#")): #comment and empty lines are ignored
                    if flag == 0:
                        flag = 1
                elif stripped:
                    flag = 0
                    data = line + data

    return data