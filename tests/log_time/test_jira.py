import subprocess
import requests
from requests.auth import HTTPBasicAuth

def test_log_time_full_success(mocker, parsed_user_data):
    username = "john.doe@example.com"
    password = "secret"
    mocker.patch("src.log_time.jira.platform.system", return_value="Linux")
    mock_subprocess = mocker.patch("src.log_time.jira.subprocess.run")
    mock_subprocess.return_value = subprocess.CompletedProcess(
        args=["ping", "-c", "1", "example.com"],
        returncode=0
    )
    mocker.patch("src.log_time.jira.prompt", side_effect=[username, password])

    mock_response = mocker.Mock()
    mock_response.json.return_value = { "result": "successfull" }
    mock_response.raise_for_status = mocker.Mock()

    mock_requests_get = mocker.patch("src.log_time.jira.requests.get", return_value=mock_response)
    mock_requests_post = mocker.patch("src.log_time.jira.requests.post", return_value=mock_response)

    from src.log_time.jira import log_time
    jira_host_name = "example.com"
    result = log_time(parsed_user_data, jira_host_name)

    assert result is True
    mock_subprocess.assert_called_once_with(
        ["ping", "-c", "1", "example.com"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )
    mock_requests_get.assert_called_once_with("https://example.com:443/rest/api/2/myself", auth=HTTPBasicAuth(username, password))
    assert mock_requests_post.call_count == 12

def test_is_reachable_success_linux(mocker):
    mocker.patch("src.log_time.jira.platform.system", return_value="Linux")
    mock_subprocess = mocker.patch("src.log_time.jira.subprocess.run")
    mock_subprocess.return_value = subprocess.CompletedProcess(
        args=["ping", "-c", "1", "example.com"],
        returncode=0
    )

    from src.log_time.jira import is_reachable
    result = is_reachable("example.com")

    assert result is True
    mock_subprocess.assert_called_once_with(
        ["ping", "-c", "1", "example.com"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )

def test_is_reachable_success_windows(mocker):
    mocker.patch("src.log_time.jira.platform.system", return_value="Windows")
    mock_subprocess = mocker.patch("src.log_time.jira.subprocess.run")
    mock_subprocess.return_value = subprocess.CompletedProcess(
        args=["ping", "-n", "1", "example.com"],
        returncode=0
    )

    from src.log_time.jira import is_reachable
    result = is_reachable("example.com")

    assert result is True
    mock_subprocess.assert_called_once_with(
        ["ping", "-n", "1", "example.com"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )

def test_is_reachable_failure(mocker):
    mocker.patch("src.log_time.jira.platform.system", return_value="Linux")
    mock_subprocess = mocker.patch("src.log_time.jira.subprocess.run")
    mock_subprocess.return_value = subprocess.CompletedProcess(
        args=["ping", "-c", "1", "example.com"],
        returncode=1
    )

    from src.log_time.jira import is_reachable
    result = is_reachable("example.com")

    assert result is False
    mock_subprocess.assert_called_once_with(
        ["ping", "-c", "1", "example.com"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )
    
def test_is_valid_authentication_success(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = { "result": "successfull" }
    mock_response.raise_for_status = mocker.Mock()
    mock_requests_get = mocker.patch("src.log_time.jira.requests.get", return_value=mock_response)

    user = "john.doe@example.com"
    password = "secret"
    auth = HTTPBasicAuth(user, password)

    from src.log_time.jira import is_valid_authentication
    result = is_valid_authentication(auth, "example.com")

    assert result is True
    mock_requests_get.assert_called_once_with("https://example.com:443/rest/api/2/myself", auth=auth)
    mock_response.raise_for_status.assert_called_once()

def test_is_valid_authentication_failure(mocker):
    mock_response = mocker.Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")

    mocker.patch("src.log_time.jira.requests.get", return_value=mock_response)
    user = "john.doe@example.com"
    password = "secret"
    auth = HTTPBasicAuth(user, password)

    from src.log_time.jira import is_valid_authentication
    result = is_valid_authentication(auth, "example.com")

    assert result is False
    mock_response.raise_for_status.assert_called_once()

def test_add_worklog(mocker, work_log):
    mock_response = mocker.Mock()
    mock_response.json.return_value = { "result": "successfull" }
    mock_response.raise_for_status = mocker.Mock()
    mock_requests_post = mocker.patch("src.log_time.jira.requests.post", return_value=mock_response)

    url = "https://example.com/test"
    user = "john.doe@example.com"
    password = "secret"
    auth = HTTPBasicAuth(user, password)

    from src.log_time.jira import add_worklog
    result = add_worklog(url, work_log, auth)

    assert result is True
    mock_requests_post.assert_called_once_with(url, auth=auth, json=work_log, timeout=90)
    mock_response.raise_for_status.assert_called_once()
