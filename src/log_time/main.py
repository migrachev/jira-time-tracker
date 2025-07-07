import sys

from . import hash
from . import user_data
from . import jira
from .mytypes import UserData
from ..config import Config
from .. import configure

command_line_arguments: list[str] = sys.argv[1:]
with_config_flag = "--config" in command_line_arguments
config: Config = Config()

try:
    if not config or with_config_flag:
        configure.do(config, with_config_flag)
    elif not with_config_flag:
        period, raw_data = user_data.get()
        print(raw_data)
        if raw_data:
            data: UserData = user_data.parse(raw_data)
            is_valid_data: bool = user_data.validate(data, period)
            if is_valid_data:
                print("\033[32m\nData is valid! We can proceed with logging!\033[0m")
                logs_hash: list[str] = hash.generate(data)
                is_successfully_logged: bool = jira.log_time(data)
                if is_successfully_logged:
                    hash.save(logs_hash)
        else:
            print("\033[33mNo information found in the input data for the defined period!\033[0m")
except KeyboardInterrupt:
    print("\033[33mInterupted by user!\033[0m")