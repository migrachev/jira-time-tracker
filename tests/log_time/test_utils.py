from pathlib import Path

def test_parse_iso_date(date_string):
    from src.log_time.utils import parse_iso_date

    parsed = parse_iso_date(date_string)
    assert parsed == (2045, 7, 15)

def test_is_valid_date(date_string, bad_date_string, bad_format_date_string):
    from src.log_time.utils import is_valid_date

    assert is_valid_date(date_string) is True
    assert is_valid_date(bad_date_string) is False
    assert is_valid_date(bad_format_date_string) is False

def test_split_work_log():
    from src.log_time.utils import split_work_log

    standard_worklog = "- 6h Do something important! TRR-1312"
    weird_worklog = " -3.5h Do something weird! TRR-321"
    messed_up_worklog = "    -0.5h    Do something nasty!           T-1       "

    assert split_work_log(standard_worklog) == ("6h", "Do something important!", "TRR-1312")
    assert split_work_log(weird_worklog) == ("3.5h", "Do something weird!", "TRR-321")
    assert split_work_log(messed_up_worklog) == ("0.5h", "Do something nasty!", "T-1")

def test_is_proper_work_week(parsed_user_data, improper_parsed_user_data_days):
    from src.log_time.utils import is_proper_work_week

    assert is_proper_work_week(parsed_user_data) is True
    assert is_proper_work_week(improper_parsed_user_data_days) is False

def test_are_jira_identifiers_valid(parsed_user_data, improper_parsed_user_data_jira):
    from src.log_time.utils import are_jira_identifiers_valid

    assert are_jira_identifiers_valid(parsed_user_data) is True
    assert are_jira_identifiers_valid(improper_parsed_user_data_jira) is False

def test_are_times_valid(parsed_user_data, improper_parsed_user_data_times):
    from src.log_time.utils import are_times_valid

    assert are_times_valid(parsed_user_data) is True
    assert are_times_valid(improper_parsed_user_data_times) is False

def test_is_fully_logged_week(parsed_user_data, improper_parsed_user_data_sum):
    from src.log_time.utils import is_fully_logged_week

    assert is_fully_logged_week(parsed_user_data) is True
    assert is_fully_logged_week(improper_parsed_user_data_sum) is False

def test_in_conflict_with_previous_execution(mocker, logs, another_logs):
    from src.log_time.utils import in_conflict_with_previous_execution
    
    mocked_open = mocker.mock_open(read_data="\n".join(logs))
    mocker.patch("builtins.open", mocked_open)

    script_dir = Path(__file__).parent
    root_dir = script_dir.parent.parent
    file_path = root_dir / "data-hash-logs.log"
    
    assert in_conflict_with_previous_execution(logs) is True
    mocked_open.assert_called_once_with(file_path, "r")
    assert in_conflict_with_previous_execution(another_logs) is False
    assert mocked_open.call_count == 2
