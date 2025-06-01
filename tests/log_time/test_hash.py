from pathlib import Path
from unittest.mock import call

from src.config import APP_DATA

def test_generate(parsed_user_data):
    from src.log_time.hash import generate

    logs = generate(parsed_user_data)
    hashes = [
        '99a0626fb1eee19aa9ef6ddb9e5db34773a161fdbf1719eba9b1e214cfd847c0',
        '68285d7cef8dad934a2907367bb28fd54aac1d1a1664dc2092f73e09faa90fb6',
        '3f2bd7137d91cc849eb8c9ab478cf24e0c1ede2e8dff2c77bfe0e2b2483d9944',
        'ab0cc68658da418e80376199edb8c9c1bb877cb26ac6b819ad427fd1f637c8de',
        '73d171eca2e10547062a1f025cb0e7877ca1d73a985244e86c10d7699e76bfd2',
        '803f2f23e389a1109c20af4f9ef0ca2a4c798ed9fc6527a02cd5455723e7c5a0',
        'f1f82782278d1a136212aa6140393a7f486cbae269de761b4b579a9d0802ed4f',
        '8d9c6e70b323781d82681fb1844054039ef469f89820f8d32874fabae493a603',
        'a7ab44ecdd4bdf6254b1561587cfa0c00467e52ed8328fbbb87b5b1a2dab51d5',
        '557362b6e59e5accbeb9b0f5dd0c896f1711776cd3c838a9053475f0329352e8',
        '8d4ca42cb97e517e33c00398521296acd4b0709754cadfa7629b7a8fad940e60',
        'cc5fddb6cb0979eb2fea455da1765c99e89c0815e6d197d08e5e0571990af109'
    ]
    
    for hash in hashes:
        assert hash in logs

def test_save(mocker, logs):
    from src.log_time.hash import save

    mocked_open = mocker.patch("builtins.open", mocker.mock_open())
    save(logs)

    file_path = APP_DATA / "data-hash-logs.log"
    mocked_open.assert_called_once_with(file_path, "w")
    
    assert call(logs[0]) in mocked_open().write.call_args_list
    assert call(logs[1]) in mocked_open().write.call_args_list
    assert call(logs[2]) in mocked_open().write.call_args_list
    assert call(logs[3]) in mocked_open().write.call_args_list
    assert call(logs[4]) in mocked_open().write.call_args_list
    assert call(logs[5]) in mocked_open().write.call_args_list
    assert call(logs[6]) in mocked_open().write.call_args_list
    assert call(logs[7]) in mocked_open().write.call_args_list
    assert call(logs[8]) in mocked_open().write.call_args_list
    assert call(logs[9]) in mocked_open().write.call_args_list
    assert call(logs[10]) in mocked_open().write.call_args_list
    assert call(logs[11]) in mocked_open().write.call_args_list