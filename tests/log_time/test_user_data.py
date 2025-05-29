import readchar

def test_validate(
        mocker, 
        logs,
        another_logs, 
        parsed_user_data, 
        improper_parsed_user_data_days, 
        improper_parsed_user_data_jira, 
        improper_parsed_user_data_sum, 
        improper_parsed_user_data_times
):
    from src.log_time.user_data import validate

    mocked_open = mocker.mock_open(read_data="\n".join(another_logs))
    mocker.patch("builtins.open", mocked_open)

    assert validate(parsed_user_data) is True
    assert validate(improper_parsed_user_data_days) is False
    assert validate(improper_parsed_user_data_jira) is False
    assert validate(improper_parsed_user_data_sum) is False
    assert validate(improper_parsed_user_data_times) is False

    mocked_open = mocker.mock_open(read_data="\n".join(logs))
    mocker.patch("builtins.open", mocked_open)

    assert validate(parsed_user_data) is False

def test_parse(raw_user_data):
    from src.log_time.user_data import parse

    parsed = parse(raw_user_data)

    assert isinstance(parsed, dict)
    for key, value in parsed.items():
        assert isinstance(key, tuple) and len(key) == 3
        assert all(isinstance(i, int) for i in key)

        assert isinstance(value, list)
        for item in value:
            assert isinstance(item, tuple) and len(item) == 3
            assert all(isinstance(i, str) for i in item)

def test_get_paste(mocker, already_logged_data_from_paste, raw_user_data):
    from src.log_time.user_data import get

    down = readchar.key.DOWN
    enter = readchar.key.ENTER
    mocker.patch("src.log_time.user_data.readchar.readkey", side_effect=[down, enter])
    mock_prompt = mocker.patch("src.log_time.user_data.prompt")
    mock_prompt.return_value = already_logged_data_from_paste
    data = get("")

    assert data == raw_user_data

def test_get_file(
    mocker,
    raw_user_data,
    already_logged_data_from_file   
):
    from src.log_time.user_data import get

    filename = "test.txt"    
    down = readchar.key.DOWN
    up = readchar.key.UP
    enter = readchar.key.ENTER
    mocker.patch("src.log_time.user_data.readchar.readkey", side_effect=[down, up, enter])
    mock_prompt = mocker.patch("src.log_time.user_data.prompt")
    mock_prompt.return_value = filename
    mocked_open = mocker.mock_open(read_data=already_logged_data_from_file)
    mocker.patch("builtins.open", mocked_open)
    data = get("")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print(data)
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print(raw_user_data)
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    assert data == raw_user_data