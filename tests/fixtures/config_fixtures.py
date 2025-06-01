import pytest

@pytest.fixture
def config():
    return """{
"jira_domain_name": "example.com",
"default_logs_location": "/home/milen/times.txt"
}"""