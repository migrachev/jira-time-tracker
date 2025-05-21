import sys
import user
import jira
import hash

jira_host_name = ""; default_file_location = ""
command_line_arguments = sys.argv[1:]
for argument in command_line_arguments:
    flag_name, flag_value = argument.split("=")
    if flag_name == "--jira" or flag_name == "-j":
        jira_host_name = flag_value
    elif flag_name == "--default-log-file-location" or flag_name == "-l":
        default_file_location = flag_value

if not jira_host_name:
    print("\033[31mMissing required flag --jira! We need to know your jira hostname to log you time!\033[0m")
else:
    data: str = user.get_data(default_file_location)

    if data:
        formatted_data = user.parse_data(data)
        logs_hash = hash.generate(formatted_data)
        is_valid_data = user.validate_data(formatted_data, logs_hash)
        if is_valid_data:
            print("\033[32mData is valid!\033[0m")
            is_successfully_logged = jira.log_time(formatted_data, jira_host_name)
            if is_successfully_logged:
                hash.save(logs_hash)