import os
import readchar
from prompt_toolkit import prompt

def getUserData(defaultFileLocation):
    options = [
        "Refer data from file.", 
        "Paste data as text."
    ]
    index = 0  # Start at the first option

    while True:
        print("How do you want to supply us with the data to process?\n")
        # Display options
        for i, option in enumerate(options):
            if i == index:
                print(f"> \033[32m{option}\033[0m")  # Highlight the selected option
            else:
                print(f"  {option}")

        key = readchar.readkey()  # Wait for key press

        if key == readchar.key.UP or key == readchar.key.LEFT:
            index = (index - 1) % len(options)  # Move selection up/left
        elif key == readchar.key.DOWN or key == readchar.key.RIGHT:
            index = (index + 1) % len(options)  # Move selection down/right
        elif key == readchar.key.ENTER or key == "\r":
            break  # Confirm selection with Enter

        print("\033c", end="")  # Clear screen for smooth UI update

    data = ""
    if index:
        data = prompt("Paste your input here!")
    else:
        fileLocation = prompt("Please provide the file location: ", default=defaultFileLocation)
        with open(fileLocation, 'r', encoding='utf-8') as dataFile:
            flag: int = -1
            iterator = reversed(list(dataFile))
            while flag < 1:
                line = next(iterator)
                stripped = line.strip()
                if stripped and (line.startswith("=") or line.startswith("#")): #comment and empty lines are ignored
                    if flag == 0:
                        flag = 1
                elif stripped:
                    flag = 0
                    data = line + data

    return data