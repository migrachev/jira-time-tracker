import readchar
from datetime import datetime, timedelta
from prompt_toolkit import prompt
from typing import Callable
from .extract_teams.utils import debounce, get_calendar_date
import pyperclip

def demand_period(
    title: str,
    label_start: str,
    label_end: str,
    invalid_period: str,
    invalid_date: str,
    date_validator: Callable[[str], bool],
    period_validator: Callable[[str, str], bool]
        
) -> tuple[str, str]:
    def infer_defaults() -> tuple[str, str]:
        today = datetime.now().date()
        last_friday = today - timedelta(days=(today.weekday() - 4) % 7)

        end_date = last_friday
        start_date = end_date - timedelta(days=4)  # Monday of the same week

        return start_date.isoformat(), end_date.isoformat()
    
    default_start, default_end = infer_defaults()
    clear_screen()
    while True:
        print(title)
        start = demand_prompt(label_start, invalid_date, date_validator, default_start, True)
        end = demand_prompt(label_end, invalid_date, date_validator, default_end, True)
        if period_validator(start, end):
            return start, end
        else:
            print(f"\033[31m{invalid_period}\033[0m")

def demand_clipboard(
        label: str,
        warn: str,
        invalid: str,
        validator: Callable[[str], bool] = lambda _x: True
) -> str:
    k = ""

    while True:
        debounced_print = debounce(print, 0.5)
        print(f"{label}: ", end='', flush=True)
        while not k == readchar.key.ENTER:
            k = readchar.readkey()
            if not k == readchar.key.ENTER:
                debounced_print(f"\033[31m{warn}\033[0m")
        value = pyperclip.paste()
        if validator(value):
            return value
        else:
            message = f"\033[31m{invalid}\033[0m"
            print(message)

def demand_prompt(
        label: str, 
        warn: str, 
        validator: Callable[[str], bool] = lambda i: True, 
        default: str = "",
        skip_clear: bool = False
) -> str:
     if not skip_clear:
         clear_screen()
     while True:
          value = prompt(f"{label}: ", default=default)
          if validator(value):
               return value
          else:
               message = f"\033[31m{warn}\033[0m"
               print(message)
               default = ""

def demand_choice(label: str, options: dict[str, str]) -> str:
     index: int = 0
     selection: str = ""
     codes = list(options.keys())

     while True:
        clear_screen()
        print(f"{label}: ")
        for i, code in enumerate(codes):
            if i == index:
                print(f"> \033[32m{options[code]}\033[0m")  # Highlight the selected option
            else:
                print(f"  {options[code]}")

        key: str = readchar.readkey() 

        if key == readchar.key.UP or key == readchar.key.LEFT:
            index = (index - 1) % len(options)
        elif key == readchar.key.DOWN or key == readchar.key.RIGHT:
            index = (index + 1) % len(options)
        elif key == readchar.key.ENTER or key == "\r":
            selection = codes[index]
            break  # Confirm selection
        
     return selection

def clear_screen():
     print("\033c", end="")  # Clear screen