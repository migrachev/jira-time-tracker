import sys
import hash
import user_data
import jira
from mytypes import UserData

jira_host_name: str = ""; default_file_location: str = ""
flag_name: str; flag_value: str
command_line_arguments: list[str] = sys.argv[1:]

for argument in command_line_arguments:
    flag_name, flag_value = argument.split("=")
    if flag_name == "--jira" or flag_name == "-j":
        jira_host_name = flag_value
    elif flag_name == "--default-log-file-location" or flag_name == "-l":
        default_file_location = flag_value

if not jira_host_name:
    print("\033[31mMissing required flag --jira! We need to know your jira hostname to log you time!\033[0m")
else:
    raw_data: str = user_data.get(default_file_location)

    if raw_data:
        data: UserData = user_data.parse(raw_data)
        logs_hash: list[str] = hash.generate(data)
        is_valid_data: bool = user_data.validate(data, logs_hash)
        if is_valid_data:
            print("\033[32mData is valid!\033[0m")
            is_successfully_logged: bool = jira.log_time(data, jira_host_name)
            if is_successfully_logged:
                hash.save(logs_hash)