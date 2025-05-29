import pytest
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

@pytest.fixture
def date_string():
    return "2045-07-15"

@pytest.fixture
def bad_format_date_string():
    return "15-07-2045"

@pytest.fixture
def bad_date_string():
    return "2045-04-31"