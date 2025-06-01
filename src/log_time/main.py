import sys

from . import hash
from . import user_data
from . import jira
from . import configure
from .mytypes import UserData
from ..config import Config

command_line_arguments: list[str] = sys.argv[1:]
with_config_flag = "--config" in command_line_arguments
config: Config = Config()

if not config or with_config_flag:
    configure.do(config, with_config_flag)
elif not with_config_flag:
    raw_data: str = user_data.get()
    if raw_data:
        data: UserData = user_data.parse(raw_data)
        is_valid_data: bool = user_data.validate(data)
        if is_valid_data:
            print("\033[32mData is valid!\033[0m")
            logs_hash: list[str] = hash.generate(data)
            is_successfully_logged: bool = jira.log_time(data)
            if is_successfully_logged:
                hash.save(logs_hash)