import pytest

@pytest.fixture
def raw_user_data():
    mocked_raw_data = """2045-07-03
- 2h Do some important stuff! IPJ-170
- 6h Requirements Workshop! ISTN-87
2045-07-04
- 8h Vacation INT-762
2045-07-05
- 0.5h Daily Scrum IPJ-101
- 1.5h Code reviews IPJ-117
- 4h Requirements Workshop! ISTN-87
- 2h Shuttle testing ISTN-221
2045-07-06
- 8h Vacation INT-762
2045-07-07
- 0.5h Daily Scrum IPJ-101
- 2h Backlog Refinement IPJ-207
- 2.5h Sprint Planning IPJ-271
- 3h Shuttle testing ISTN-221"""

    return mocked_raw_data

@pytest.fixture
def parsed_user_data():
    day_one = (2045, 7, 3)
    day_two = (2045, 7, 4)
    day_three = (2045, 7, 5)
    day_four = (2045, 7, 6)
    day_five = (2045, 7, 7)

    day_one_activities = [
        ("2h", "Do some important stuff!", "IPJ-170"),
        ("6h", "Requirements Workshop!", "ISTN-87")
    ]
    day_two_activities = [
        ("8h", "Vacation", "INT-762")
    ]
    day_three_activities = [
        ("0.5h", "Daily Scrum", "IPJ-101"),
        ("1.5h", "Code reviews", "IPJ-117"),
        ("4h", "Requirements Workshop!", "ISTN-87"),
        ("2h", "Shuttle testing", "ISTN-221")
    ]
    day_four_activities = [
        ("8h", "Vacation", "INT-762")
    ]
    day_five_activities = [
        ("0.5h", "Daily Scrum", "IPJ-101"),
        ("2h", "Backlog Refinement", "IPJ-207"),
        ("2.5h", "Sprint Planning", "IPJ-271"),
        ("3h", "Shuttle testing", "ISTN-221")
    ]
    
    mocked_parsed_user_data = {}
    mocked_parsed_user_data[day_one] = day_one_activities
    mocked_parsed_user_data[day_two] = day_two_activities
    mocked_parsed_user_data[day_three] = day_three_activities
    mocked_parsed_user_data[day_four] = day_four_activities
    mocked_parsed_user_data[day_five] = day_five_activities

    return mocked_parsed_user_data

@pytest.fixture
def improper_parsed_user_data_days():
    day_one = (2045, 7, 4)
    day_two = (2045, 7, 5)
    day_three = (2045, 7, 6)
    day_four = (2045, 7, 7)
    day_five = (2045, 7, 8)

    day_one_activities = [
        ("2h", "Do some important stuff!", "IPJ-170"),
        ("6h", "Requirements Workshop!", "ISTN-87")
    ]
    day_two_activities = [
        ("8h", "Vacation", "INT-762")
    ]
    day_three_activities = [
        ("0.5h", "Daily Scrum", "IPJ-101"),
        ("1.5h", "Code reviews", "IPJ-117"),
        ("4h", "Requirements Workshop!", "ISTN-87"),
        ("2h", "Shuttle testing", "ISTN-221")
    ]
    day_four_activities = [
        ("8h", "Vacation", "INT-762")
    ]
    day_five_activities = [
        ("0.5h", "Daily Scrum", "IPJ-101"),
        ("2h", "Backlog Refinement", "IPJ-207"),
        ("2.5h", "Sprint Planning", "IPJ-271"),
        ("3h", "Shuttle testing", "ISTN-221")
    ]
    
    mocked_parsed_user_data = {}
    mocked_parsed_user_data[day_one] = day_one_activities
    mocked_parsed_user_data[day_two] = day_two_activities
    mocked_parsed_user_data[day_three] = day_three_activities
    mocked_parsed_user_data[day_four] = day_four_activities
    mocked_parsed_user_data[day_five] = day_five_activities

    return mocked_parsed_user_data

@pytest.fixture
def improper_parsed_user_data_times():
    day_one = (2045, 7, 3)
    day_two = (2045, 7, 4)
    day_three = (2045, 7, 5)
    day_four = (2045, 7, 6)
    day_five = (2045, 7, 7)

    day_one_activities = [
        ("2h", "Do some important stuff!", "IPJ-170"),
        ("2h", "Requirements Workshop!", "ISTN-87")
    ]
    day_two_activities = [
        ("8", "Vacation", "INT-762")
    ]
    day_three_activities = [
        ("0.5h", "Daily Scrum", "IPJ-101"),
        ("1.5h", "Code reviews", "IPJ-117"),
        ("4h", "Requirements Workshop!", "ISTN-87"),
        ("2h", "Shuttle testing", "ISTN-221")
    ]
    day_four_activities = [
        ("8h", "Vacation", "INT-762")
    ]
    day_five_activities = [
        ("0.5h", "Daily Scrum", "IPJ-101"),
        ("2h", "Backlog Refinement", "IPJ-207"),
        ("2.5h", "Sprint Planning", "IPJ-271"),
        ("3h", "Shuttle testing", "ISTN-221")
    ]
    
    mocked_parsed_user_data = {}
    mocked_parsed_user_data[day_one] = day_one_activities
    mocked_parsed_user_data[day_two] = day_two_activities
    mocked_parsed_user_data[day_three] = day_three_activities
    mocked_parsed_user_data[day_four] = day_four_activities
    mocked_parsed_user_data[day_five] = day_five_activities

    return mocked_parsed_user_data

@pytest.fixture
def improper_parsed_user_data_jira():
    day_one = (2045, 7, 3)
    day_two = (2045, 7, 4)
    day_three = (2045, 7, 5)
    day_four = (2045, 7, 6)
    day_five = (2045, 7, 7)

    day_one_activities = [
        ("2h", "Do some important stuff!", ""),
        ("2h", "Requirements Workshop!", "ISTN-")
    ]
    day_two_activities = [
        ("8h", "Vacation", "INT")
    ]
    day_three_activities = [
        ("0.5h", "Daily Scrum", "IPJ-101"),
        ("1.5h", "Code reviews", "IPJ-117"),
        ("4h", "Requirements Workshop!", "ISTN-87"),
        ("2h", "Shuttle testing", "ISTN-221")
    ]
    day_four_activities = [
        ("8h", "Vacation", "INT-762")
    ]
    day_five_activities = [
        ("0.5h", "Daily Scrum", "IPJ-101"),
        ("2h", "Backlog Refinement", "IPJ-207"),
        ("2.5h", "Sprint Planning", "IPJ-271"),
        ("3h", "Shuttle testing", "ISTN-221")
    ]
    
    mocked_parsed_user_data = {}
    mocked_parsed_user_data[day_one] = day_one_activities
    mocked_parsed_user_data[day_two] = day_two_activities
    mocked_parsed_user_data[day_three] = day_three_activities
    mocked_parsed_user_data[day_four] = day_four_activities
    mocked_parsed_user_data[day_five] = day_five_activities

    return mocked_parsed_user_data

@pytest.fixture
def improper_parsed_user_data_sum():
    day_one = (2045, 7, 3)
    day_two = (2045, 7, 4)
    day_three = (2045, 7, 5)
    day_four = (2045, 7, 6)
    day_five = (2045, 7, 7)

    day_one_activities = [
        ("2h", "Do some important stuff!", "IPJ-170"),
        ("1h", "Requirements Workshop!", "ISTN-87")
    ]
    day_two_activities = [
        ("8h", "Vacation", "INT-762")
    ]
    day_three_activities = [
        ("0.5h", "Daily Scrum", "IPJ-101"),
        ("1.5h", "Code reviews", "IPJ-117"),
        ("4h", "Requirements Workshop!", "ISTN-87"),
        ("2h", "Shuttle testing", "ISTN-221")
    ]
    day_four_activities = [
        ("8h", "Vacation", "INT-762")
    ]
    day_five_activities = [
        ("0.5h", "Daily Scrum", "IPJ-101"),
        ("2h", "Backlog Refinement", "IPJ-207"),
        ("2.5h", "Sprint Planning", "IPJ-271"),
        ("3h", "Shuttle testing", "ISTN-221")
    ]
    
    mocked_parsed_user_data = {}
    mocked_parsed_user_data[day_one] = day_one_activities
    mocked_parsed_user_data[day_two] = day_two_activities
    mocked_parsed_user_data[day_three] = day_three_activities
    mocked_parsed_user_data[day_four] = day_four_activities
    mocked_parsed_user_data[day_five] = day_five_activities

    return mocked_parsed_user_data
