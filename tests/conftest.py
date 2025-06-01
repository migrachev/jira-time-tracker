import pytest
from datetime import date
from .fixtures.user_fixtures import parsed_user_data
from .fixtures.user_fixtures import raw_user_data
from .fixtures.user_fixtures import improper_parsed_user_data_days
from .fixtures.user_fixtures import improper_parsed_user_data_jira
from .fixtures.user_fixtures import improper_parsed_user_data_times
from .fixtures.user_fixtures import improper_parsed_user_data_sum
from .fixtures.logs_fixtures import logs
from .fixtures.logs_fixtures import another_logs
from .fixtures.input_fixtures import already_logged_data_from_file
from .fixtures.input_fixtures import already_logged_data_from_paste
from .fixtures.input_fixtures import new_data_from_file
from .fixtures.input_fixtures import new_data_from_paste
from .fixtures.config_fixtures import config

@pytest.fixture
def work_log():
    day = (2045, 7, 3)
    work_date = date(*day)
    started = f"{work_date.isoformat()}T10:00:00.000+0000"
    return {
        "started": started,
        "comment": "Requirements Workshop!",
        "timeSpentSeconds": "ISTN-87"
    }

@pytest.fixture
def date_string():
    return "2045-07-15"

@pytest.fixture
def bad_format_date_string():
    return "15-07-2045"

@pytest.fixture
def bad_date_string():
    return "2045-04-31"