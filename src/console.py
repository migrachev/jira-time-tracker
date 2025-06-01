import readchar
from prompt_toolkit import prompt
from typing import Callable

def demand_prompt(
        label: str, 
        warn: str, 
        validator: Callable[[str], bool] = lambda i: True, 
        default: str = ""
) -> str:
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

def test(validator: Callable[[str], bool]):
    print(validator)