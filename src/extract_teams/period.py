from ..console import demand_period
from ..log_time.utils import is_valid_date, is_valid_period

def get() -> tuple[str, str]:
    title: str = "\033[34mWhat is the period you want to extract data for?\033[0m"
    label_start: str = "Enter the start of the period you want to extract (yyyy-mm-dd)"
    label_end: str = "Enter the end of the period you want to extract (yyyy-mm-dd)"
    invalid_date: str = "Your input is not a valid date. Make sure you provide date in yyyy-mm-dd format."
    invalid_period: str = "The period you entered is invalid. Please try again!"
    
    start, end = demand_period(
        title=title,
        label_start=label_start,
        label_end=label_end,
        invalid_date=invalid_date,
        invalid_period=invalid_period,
        date_validator=is_valid_date,
        period_validator=is_valid_period
    )

    return start, end