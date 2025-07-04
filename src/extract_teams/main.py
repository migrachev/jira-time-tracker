import sys

from . import teams_data
from ..config import Config
from .. import configure
from . import period

command_line_arguments: list[str] = sys.argv[1:]
with_config_flag = "--config" in command_line_arguments
config: Config = Config()

if not config or with_config_flag:
    configure.do(config, with_config_flag)
elif not with_config_flag:
    start, end = period.get()
    raw_data = teams_data.get()
    preped_data = teams_data.prepare(raw_data, (start, end))
    parsed_data = teams_data.parse(preped_data)
    teams_data.output(parsed_data, (start, end))